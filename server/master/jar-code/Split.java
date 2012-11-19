import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.ArrayList;
import java.util.Scanner;

import javax.imageio.ImageIO;

/**
*Usage: Split <image name> <output dir>
*/
public class Split {
	public static void main(String [] args) throws InterruptedException, Exception {
		int argc = args.length;
		if (argc != 2)
			System.out.println("Usage: java -jar <image filename> <split images output dir>");
		else {
			String image_file_name = args[0];
			String output_dr = args[1];
			//split("image_new_output.txt","image_new.png");
			split(image_file_name.substring(0, image_file_name.indexOf(".png"))+"_output.txt", image_file_name, output_dr);
		}
	}
	public static String[] split(String textFileName, String imageFileName, String outdir) throws InterruptedException, Exception {
		String command = "java -jar IDT.jar -f " + imageFileName + " -o text";
		System.out.println(command);
		Process process = Runtime.getRuntime().exec(command.split(" "));
		if (process.waitFor() != 0) {
			throw new Exception("IDT could not run");
		}
		Scanner scan = new Scanner(new File(textFileName));
		BufferedImage img = ImageIO.read(new File(imageFileName));
		int numOfSplits = scan.nextInt();
        	BufferedImage images[] = new BufferedImage[numOfSplits];
        	String [] filenames = new String[numOfSplits];
		ArrayList <Crop>crops = new ArrayList<Crop>();
		int count = 0;
		scan.nextLine();
		
		while(scan.hasNext()) {
			String line = scan.nextLine();
			String [] arr = line.split(" ");
			int x = Integer.valueOf(arr[0]);
			if (x < 0)
				x = 0;
			int y = Integer.valueOf(arr[1]);	
			if (y < 0)
				y = 0;
			int height = Integer.valueOf(arr[2]);
			int width = Integer.valueOf(arr[3]);
			crops.add(new Crop(new Point(x, y), width, height));
		}
		for(Crop c : crops) {
			Point p = c.topLeft;
			int x = p.x;
			int y = p.y;
			int width = c.width;
			int height = c.height;
			if (x + c.width >= img.getWidth()) {
				width = img.getWidth() - x - 1;
			}
			if (y + c.height >= img.getHeight()) {
				height = img.getHeight() - y - 1;
			}
			images[count] = new BufferedImage(width, height, img.getType());
			Graphics2D gr = (Graphics2D)images[count].getGraphics();
			BufferedImage subImag = img.getSubimage(x, y, width, height);
			gr.drawImage(subImag, 0, 0, width, height, null );
			gr.dispose();
			count++;
		}
		for (int i = 0; i < images.length; i++) {
            Crop cr = crops.get(i);
			ImageIO.write(images[i], "png", new File(outdir+"img" + i + "_" + cr.topLeft.x + "_" + cr.topLeft.y + "_" + cr.height + "_" + cr.width +"_.png"));
	        filenames[i] = "img" + i + ".png";
        }
        return filenames;
	}
	private static class Crop implements Comparable<Crop> {
		Point topLeft;
		int width;
		int height;
		public Crop(Point topLeft, int w, int h) {
			this.topLeft = topLeft;
			width = w;
			height = h;
		}
		@Override
		public int compareTo(Crop o) {
			Point other = o.topLeft;
			if (this.topLeft.y < other.y) {
				return -1;
			} else if(this.topLeft.x > other.x)
				return 1;
			return 0;
				
		}
		public String toString() {
			return "["+ topLeft.x + ", " + topLeft.y + "] and ("+width+", " + height + ")";
		}
	}
}
