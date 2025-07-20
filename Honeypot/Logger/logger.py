from mitmproxy import ctx

class TrafficLogger:
    def __init__(self):
        self.log_file = open("traffic_log.txt","a") 
    def response(self,flow):
        self.log_file.write("=====================\n")
        now = datetime().now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_file.write(f"[{now}]\n")
        self.log_file.write(f"Request: {flow.request.method} {flow.request.url}\n")
        self.log_file.write(f"Response:{flow.response.status_code}\n")
        self.log_file.write("=====================\n")
        self.log_file.flush() 
    def done(self):
        self.log_file.close()
        
addons = [
    TrafficLogger()
]
