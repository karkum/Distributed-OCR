import java.io.OutputStream;
import java.io.InputStream;
import java.net.URLConnection;
import java.net.URL;
import java.net.Socket;

public class ClientTest {
    private final String CrLf = "\r\n";  
//    private final String host = "ec2-50-16-136-236.compute-1.amazonaws.com";
    private final String host = "jtestloadbalancer-1918726476.us-east-1.elb.amazonaws.com";
 
    public static void main(String[] args) {
    	ClientTest main = new ClientTest();
        main.httpConn();
    }

    private void httpConn() {
        URLConnection conn = null;
        OutputStream os = null;
        InputStream is = null;

        try { 
        	URL url = new URL("http://" + host + "/cgi-bin/upload.py"); 
            conn = url.openConnection();
            conn.setDoOutput(true);

            String postData = "";

            InputStream imgIs = getClass().getResourceAsStream("/test.png");
            byte[] imgData = new byte[imgIs.available()];
            imgIs.read(imgData);

            String message1 = "";
            message1 += "-----------------------------4664151417711" + CrLf;
            message1 += "Content-Disposition: form-data; name=\"datafile\"; filename=\"test.png\""
                    + CrLf;
            message1 += "Content-Type: image/jpeg" + CrLf;
            message1 += CrLf;

            // the image is sent between the messages in the multipart message.

            String message2 = "";
            message2 += CrLf + "-----------------------------4664151417711--"
                    + CrLf;

            conn.setRequestProperty("Content-Type",
                    "multipart/form-data; boundary=---------------------------4664151417711");
            // might not need to specify the content-length when sending chunked
            // data.
            conn.setRequestProperty("Content-Length", String.valueOf((message1
                    .length() + message2.length() + imgData.length)));
 
            os = conn.getOutputStream();
 
            os.write(message1.getBytes());

            // SEND THE IMAGE
            int index = 0;
            int size = 1024;
            do { 
                if ((index + size) > imgData.length) {
                    size = imgData.length - index;
                }
                os.write(imgData, index, size);
                index += size;
            } while (index < imgData.length); 
            
            os.write(message2.getBytes());
            os.flush();
 
            is = conn.getInputStream();

            char buff = 512;
            int len;
            byte[] data = new byte[buff];
            do { 
                len = is.read(data);

                if (len > 0) {
                    System.out.println(new String(data, 0, len));
                }
            } while (len > 0);
 
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            System.out.println("Close connection");
            try {
                os.close();
            } catch (Exception e) {
            }
            try {
                is.close();
            } catch (Exception e) {
            }
            try {

            } catch (Exception e) {
            }
        }
    }
}