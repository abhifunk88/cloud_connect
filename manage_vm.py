from cloud_mgmt import CloudMgmt


obj = CloudMgmt('stub')
obj.launch_vm()
obj.stop_vm([19899, 81772])
obj.terminate_vm([19899, 81772])
obj.start_vm([19899, 81772])
obj.list_vm()
obj.connect_vm("127.0.0.1")
obj.launch_db("127.0.0.1")
