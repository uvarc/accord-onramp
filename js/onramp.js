async function validateIp(ip) {
    try {
      const validate = await axios.get('https://06iteam4j8.execute-api.us-east-1.amazonaws.com/api/validate/' + ip);
      getMetaAccess();
      if (validate.data.status == 'true') {
        status = validate.data.status;
        campus = validate.data.institution;
        document.getElementById("portal-btn").classList.remove("hide");
        document.getElementById("ip-status").classList.remove("hide");
        document.getElementById("campus").textContent = campus;
  
      } else {
        document.getElementById("ip-status-bad").classList.remove("hide");
        document.getElementById("ip-status-bad-text").innerHTML = "Your IP address <b><code><span id='myip'>" + ip + "</span></code></b> is not authorized to access ACCORD. Please make sure you are accessing this system from your campus network or campus VPN.";
      }
    } catch (error) {
      console.error(error);
    }
  };
  
  async function getIpClient() {
      try {
          const response = await axios.get('https://api.ipify.org?format=json');
          ip = response.data.ip;
          validateIp(ip);
          document.getElementById("myip").textContent = response.data.ip;
      } catch (error) {
          console.error(error);
      }
  };
  
  async function getMetaAccess() {
    try {
      const instance = axios.create();
      instance.defaults.timeout = 100;
      const getaccess = await instance.get('https://eapi.opswatgears.com:11369/opswat/devinfo?callback=js0');
      // If success
      document.getElementById("ma-success").classList.remove("hide");
    } catch (error) {
      // If error
      if (!error.status) {
        document.getElementById("ma-failure").classList.remove("hide");
        document.getElementById("portal-btn").classList.add("hide");
      }
    }
  };
  
  function checkStatusMessages() {
      $.getJSON('https://47tpa1dam4.execute-api.us-east-1.amazonaws.com/api/accord/messages', function(data) {
          var messageData = '';
          $.each(data, function(key, value) {
              var messageBody = value.body;
              var messageLength = messageBody.length;
              if ( messageLength < 22 ) {
                  $("#status-message").hide();
              } else {
                  $("#status-message").show();
                  messageData += '<i class="fas fa-exclamation-triangle"></i>';
                  messageData += value.body;
                  $('#status-message-content').html(messageData);
              }
          });
      });
  };
  
  $(document).ready(function() {
    $("#status-message").hide();
    checkStatusMessages();
    setInterval(checkStatusMessages, 30000);
    getIpClient();
  });
  