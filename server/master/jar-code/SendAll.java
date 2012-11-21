import java.awt.image.BufferedImage;
import java.awt.image.RenderedImage;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.Scanner;

import javax.imageio.ImageIO;


public class SendAll {
	private final static String CrLf = "\r\n";
	// private final String host = "ec2-50-16-136-236.compute-1.amazonaws.com";
	private final String host = "jtestloadbalancer-1918726476.us-east-1.elb.amazonaws.com";

	public static void main(String[] args) {
		int argc = args.length;
		if (argc != 1)
			System.out.println("Usage: java -jar <images directory>");
		else {
			String dir = args[0];
			SendAll s = new SendAll();
			s.sendAll(dir);
		}
	}

	private void sendAll(String directory) {

		File dir = new File(directory);
		File[] files = dir.listFiles();
		ArrayList<URLConnection> connections = new ArrayList<URLConnection>();
		OutputStream os = null;
		for (File file : files) {
			try {
				URLConnection conn = null;
				if (file == null) {
					System.out.println("FILE WAS NULL\n");
				}
				//System.out.println(file.getAbsolutePath());
				URL url = new URL("http://" + host + "/cgi-bin/upload.py");
				conn = url.openConnection();
				conn.setDoOutput(true);
				connections.add(conn);
				//InputStream imgIs = getClass().getResourceAsStream(
				//		file.getAbsolutePath());
				//byte[] imgData = new byte[imgIs.available()];
				BufferedImage bufferedImage = ImageIO.read(file);
				ByteArrayOutputStream baos = new ByteArrayOutputStream();
				ImageIO.write((RenderedImage)bufferedImage, "png", baos);
				byte[]imgData = baos.toByteArray();

				//WritableRaster raster = bufferedImage.getRaster();
				//DataBufferByte data = (DataBufferByte)raster.getDataBuffer();
				//byte[] imgData = data.getData();
				//imgIs.read(imgData);

				String message1 = "";
				message1 += "-----------------------------4664151417711" + CrLf;
				message1 += "Content-Disposition: form-data; name=\"datafile\"; filename=\""
						+ file.getAbsolutePath() + "\"" + CrLf;
				message1 += "Content-Type: image/png" + CrLf;
				message1 += CrLf;

				// the image is sent between the messages in the multipart
				// message.

				String message2 = "";
				message2 += CrLf
						+ "-----------------------------4664151417711--" + CrLf;

				conn.setRequestProperty("Content-Type",
						"multipart/form-data; boundary=---------------------------4664151417711");
				// might not need to specify the content-length when sending
				// chunked data.

				conn.setRequestProperty(
						"Content-Length",
						String.valueOf((message1.length() + message2.length() + imgData.length)));
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
			} catch (Exception e) {
				e.printStackTrace();
			} finally {
				//System.out.println("Close connection");
				try {
					os.close();
				} catch (Exception e) {
					
				}
			}
		}
		ArrayList<String>output = new ArrayList<String>();
		for (URLConnection conn : connections) {
			InputStream is = null;
			try {
				is = conn.getInputStream();

				char buff = 1024;
				int len;
				byte[] data = new byte[buff];
				do {
					len = is.read(data);
					if (len > 0) {
					//	System.out.println("Adding: " + new String(data, 0, len));
						output.add(new String(data, 0, len));
					}
				} while (len > 0);
			} catch (Exception e) {
				
			}
			finally {
				try {
					is.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		TesseractInfo[] infos = new TesseractInfo[files.length];
		int i = 0;
		for (String str : output) {
			try {
				if (str != null && str.length() != 0) {
					Scanner scan = new Scanner(str);
					String firstLine = scan.nextLine();
					String [] numbers = firstLine.split(" ");
					int x = Integer.valueOf(numbers[0]);
					int y = Integer.valueOf(numbers[1]);
					int w = Integer.valueOf(numbers[2]);
					int h = Integer.valueOf(numbers[3]);
					StringBuffer buffer = new StringBuffer();
					while (scan.hasNext()) {
						buffer.append(scan.nextLine());
					}
					String data = buffer.toString();
					TesseractInfo info = new TesseractInfo(x, y, w, h, data);
					infos[i++] = info;
				}
			
		} catch (Exception e) {
		//	System.out.println("Error parsing image.\n");
			continue;
		}
		}
		
		ImageConstructor construct = new ImageConstructor(infos);
		System.out.println(construct.getFinalString());
	}
}
