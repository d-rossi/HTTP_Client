import subprocess
import json

def test_httpc_curl(httpc_command, curl_command):
	print(f"httpc:	{httpc_command}")
	print(f"cURL:	{curl_command}\n")
	httpc_result = subprocess.check_output(httpc_command.split()).decode()	#split will not work if data or header has space
	curl_result = subprocess.check_output(curl_command.split()).decode()
	httpc_result_json = json.loads(httpc_result)
	curl_result_json = json.loads(curl_result)

	if httpc_result_json["args"]:
	    for k, v in httpc_result_json["args"].items():
	        print(f"Compare httpc and curl ARGS {k} EQUALS {curl_result_json['args'][k]}: {v == curl_result_json['args'][k]}")

	if "files" in httpc_result_json and httpc_result_json["files"]:
	    print(f"Compare httpc FILES {httpc_result_json['files']} EQUALS curl FILES {curl_result_json['files']}: {httpc_result_json['files'] == curl_result_json['files']}")

	if "data" in httpc_result_json and httpc_result_json["data"]:
	    print(f"Compare httpc DATA {httpc_result_json['data']} EQUALS curl DATA {curl_result_json['data']}: {httpc_result_json['data'] == curl_result_json['data']}")

	for k, v in httpc_result_json["headers"].items():
		if k in ["X-Amzn-Trace-Id", "Fly-Dispatch-Start", "Fly-Request-Id", "X-Request-Start"]:
			continue
		print(f"Compare if httpc {k} {v} EQUALS curl {k} {curl_result_json['headers'][k]}: {v == curl_result_json['headers'][k]}")

	print(f"Compare if httpc ORIGIN {httpc_result_json['origin']} EQUALS curl ORIGIN {curl_result_json['origin']}: {httpc_result_json['origin'] == curl_result_json['origin']}")
	print(f"Compare if httpc URL {httpc_result_json['url']} EQUALS curl URL {curl_result_json['url']}: {httpc_result_json['url'] == curl_result_json['url']}\n")


#TEST 1: GET REQUEST TEST
print("############################GET REQUEST TEST##############################")
httpc_command = 'python httpc.py get http://httpbin.org/get?course=networking&assignment=1'
curl_command = 'curl -s --request GET http://httpbin.org/get?course=networking&assignment=1'
test_httpc_curl(httpc_command, curl_command)

# #TEST 2: POST REQUEST TEST
print("############################POST REQUEST TEST##############################")
httpc_command = "python httpc.py post -h name:john -h age:35 -d Test http://httpbin.org/post"
curl_command = "curl -s --request POST --header content-type:application/json --header name:john --header age:35 --header Connection:close --data-raw Test http://httpbin.org/post"
test_httpc_curl(httpc_command, curl_command)

# #TEST 3: POST REQUEST TEST WITH FILE
print("############################POST REQUEST TEST WITH FILE##############################")
httpc_command = "python httpc.py post -h name:john -h age:35 -f test3.txt http://httpbin.org/post"
curl_command = "curl -s --request POST --header content-type:application/json --header name:john --header age:35 --header Connection:close --data-binary @test3.txt http://httpbin.org/post"
test_httpc_curl(httpc_command, curl_command)
