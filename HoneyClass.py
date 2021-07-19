import paramiko
import threading
import socket
import random
import json
import pickle
import os
import re

from PySide2 import QtGui, QtWidgets
from collections import Counter
from ip2geotools.databases.noncommercial import DbIpCity
from ip2geotools import errors

class SSHInterface(paramiko.ServerInterface):
    def __init__(self, update_pass_func, password_count, data_lock):
        self.pass_count = password_count
        self.lock = data_lock
        self.update_pass_func = update_pass_func

    def check_auth_password(self, username, password):
        strpd_pass = password.strip()

        if strpd_pass != "":
            with self.lock:
                self.pass_count[strpd_pass] += 1

            self.update_pass_func()
            
        return paramiko.AUTH_FAILED

class HoneySession(threading.Thread):
    def __init__(self, client_socket, update_pass_func, password_count, data_lock, path):
        super(HoneySession, self).__init__()
        self.transport_object = paramiko.Transport(client_socket)
        self.transport_object.add_server_key(paramiko.RSAKey(filename=path + "/rsa_key.key"))
        self.server = SSHInterface(update_pass_func, password_count, data_lock)
        self.daemon = True

    def run(self):
        self.transport_object.start_server(server=self.server)

class HoneyManager(threading.Thread):
    def __init__(self, ui, path):
        super(HoneyManager, self).__init__()
        self.loc_lock = threading.Lock()
        self.pass_lock = threading.Lock()
        self.list_model = ui.get_scroll_view()
        self.error_label = ui.get_error_label()
        self.path = path
        self.daemon = True

        if os.path.exists(path + "/data.pickle"):
            storage_tup = pickle.load(open(path + "/data.pickle", "rb"))
            self.location_dct, self.location_lst, self.pass_count, self.api_key = storage_tup

            if self.pass_count:
                self._update_pass_count()
        else:
            self.location_dct = {}
            self.location_lst = []
            self.pass_count = Counter()
            self.api_key = 'free'
        
    def run(self):
        session_lst = []
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sckt.bind(('', 22))
        sckt.listen(5)

        while True:
            clnt_sckt, clnt_data = sckt.accept()
            new_session = HoneySession(clnt_sckt, self._update_pass_count, self.pass_count, self.pass_lock, self.path)
            new_session.start()
            session_lst.append(new_session)
            handle_loc = threading.Thread(target=self._handle_location(clnt_data[0]), daemon=True)
            handle_loc.start()

            while len(session_lst) > 20:
                del_seshs = []

                for sesh in session_lst:
                    if not sesh.is_alive():
                        del_seshs.append(sesh)

                for sesh in del_seshs:
                    session_lst.remove(sesh)

    def loc_on_click(self):
        CONFIRM_DELETE = 16384

        if self._get_confirmation_dialog() == CONFIRM_DELETE:
            with self.loc_lock and self.pass_lock:
                self.location_dct.clear()
                self.location_lst.clear()

            self.save_data()
            
            with open(self.path + '/active_locations.json', 'w+') as json_file:
                json_file.write("{}")

    def pass_on_click(self):
        CONFIRM_DELETE = 16384

        if self._get_confirmation_dialog() == CONFIRM_DELETE:
            with self.pass_lock and self.loc_lock:
                self.pass_count.clear()

            self.save_data()
            self.list_model.clear()

    def api_on_click(self):
        key, ok_clicked = QtWidgets.QInputDialog.getText(QtWidgets.QWidget(), 'Enter API Key', "DB-IP API Key ('free' is default)")

        if ok_clicked and len(key) < 50:
            key = re.sub(r'\W+', '', str(key))
            self.api_key = key
            
    def save_data(self):
        with self.loc_lock and self.pass_lock:
            storage_tup = (self.location_dct, self.location_lst, self.pass_count, self.api_key)
            pickle.dump(storage_tup, open(self.path + "/data.pickle", "w+b" ))

    def _get_confirmation_dialog(self):
        dialog = QtWidgets.QMessageBox()
        dialog.setIcon(QtWidgets.QMessageBox.Question)
        dialog.setWindowTitle("Confirm Data Erase")
        dialog.setText("Are you sure?")
        dialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        return dialog.exec()

    def _lookup_error_message(self, msg):
        self.error_label.setText(msg)

    def _handle_location(self, ip):
        # ip_str = str(random.randint(1, 191)) + '.' + str(random.randint(1, 225)) + '.' + str(random.randint(0, 255)) + '.'  + str(random.randint(1, 254))
        loc_val = self._resolve_ip_loc(ip)

        if loc_val:
            loc_key = str(loc_val['lng']) + str(loc_val['lat'])

            with self.loc_lock:
                self.location_dct[loc_key] = loc_val
                self.location_lst.append(loc_key)

                if len(self.location_lst) > 100:
                    rmvd_key = self.location_lst.pop(0)

                    try:
                        self.location_dct.pop(rmvd_key)
                    except KeyError:
                        pass
                
                self._update_map()

    def _resolve_ip_loc(self, ip):
        try:
            lookup = DbIpCity.get(ip, api_key=self.api_key)
            loc_str = str(lookup.country) + ' - ' + str(lookup.city) + ', ' + str(lookup.region)

            if lookup.latitude == None or lookup.latitude == None:
                return None
            
            self.error_label.setText("")

            return ({ "lat" : float(lookup.latitude), "lng" : float(lookup.longitude), "desc" : loc_str })
        
        except errors.PermissionRequiredError:
            self._lookup_error_message('IP lookup failed. Likely an issue with API key.')

        except errors.InvalidRequestError:
            self._lookup_error_message('IP lookup failed. Free lookup rate likely exceeded.')
        
        except Exception:
            return None
        
    def _update_map(self):
        json_str = json.dumps(self.location_dct)

        with open(self.path + '/active_locations.json', 'w+') as json_file:
            json_file.write(json_str)

    def _update_pass_count(self):
        pass_lst = []

        with self.pass_lock:
            pass_lst = self.pass_count.most_common(100)
            
            tot_psswds = len(self.pass_count)

            if tot_psswds > 5000:
                del_key = None

                for key in self.pass_count:
                    if self.pass_count[key] == 1:
                        del_key = key
                        break

                if del_key:
                    self.pass_count.pop(del_key)

        if pass_lst:
            for i in range(self.list_model.rowCount()):
                self.list_model.item(i).setText(str(i+1) + '. ' + pass_lst[i][0] + ' ' + str(pass_lst[i][1]))

            for i in range(self.list_model.rowCount(), len(pass_lst)):
                item = QtGui.QStandardItem(str(i+1) + '. ' + pass_lst[i][0] + ' ' + str(pass_lst[i][1]))
                self.list_model.appendRow(item)
