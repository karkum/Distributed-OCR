import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;


public class ImageConstructor 
{
	private TesseractInfo[] infoArray;
	
	
	public ImageConstructor(TesseractInfo[] info)
	{
		this.infoArray = info;
	}
	
	
	public String getFinalString()
	{
		int minY = Integer.MAX_VALUE;
		int maxY = Integer.MIN_VALUE;
		for (TesseractInfo info : infoArray) {
			if (info.y < minY)
				minY = info.y;
			if (info.y + info.height > maxY) {
				maxY = info.y + info.height;
			}
		}
		
		int newLines = infoArray[0].data.split("\n").length;
		int lineHeight = infoArray[0].height / newLines;
		int numBins = ((maxY - minY) / lineHeight) + 1;
		
		
		List<List<Pair>> strList = new ArrayList<List<Pair>>();
		for (int i = 0; i < numBins; i++) {
			strList.add(new ArrayList<Pair>());
		}
		
		for (TesseractInfo info : infoArray) {
			int initBin = (info.y - minY) / lineHeight;
			
			String[] lines = info.data.split("\n");
			for (int i = 0; i < lines.length; i++) {
				String line = lines[i];
				strList.get(initBin + i).add(new Pair(line, info.x));
			}
		}
		
		for (List<Pair> list : strList) {
			Collections.sort(list, new Comparator<Pair>() {
				@Override
				public int compare(Pair o1, Pair o2) {
					return o1.x - o2.x;
				}
			});
		}
		
		StringBuilder sb = new StringBuilder();
		for (List<Pair> line : strList) {
			for (Pair p : line) {
				sb.append(p.data);
				sb.append(' ');
			}
			sb.append('\n');
		}
		
		return sb.toString(); 
	} 

	private class Pair {
		String data;
		int x;
		
		Pair(String data, int x) {
			this.data = data; this.x = x;
		}
	}
	

}
