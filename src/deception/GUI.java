package deception;
import java.io.*;
import java.util.ArrayList;

import javax.sound.sampled.*;
import javax.swing.JFrame;

public class GUI {
	static interval[]intInts, descInts;
	static ArrayList<interval> convo; 
	static ArrayList<sentence> sents;

	public static void main(String[] args) throws IOException, UnsupportedAudioFileException, LineUnavailableException {
		
		intInts = toIntervalArray(args[0], false); //Create interrogator interval array
		descInts = toIntervalArray(args[1], true); //Create describer intervals array
		convo = createConversation(descInts, intInts); //Merge interrogator and describer intervals into conversation 
		sents = createSentList(convo); //Parse convo intervals into sentences 
		
		AudioInputStream intAudio = AudioSystem.getAudioInputStream(new File(args[2]));
		AudioInputStream descAudio = AudioSystem.getAudioInputStream(new File(args[3]));
	
		
		
		plot Plot = new plot(sents, descInts, intInts, convo, descAudio, intAudio);
		JFrame Frame = new JFrame("Interrogator and Describer Speech");
		Frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		Frame.add(Plot);
		Frame.setSize(500,200);
		Frame.setVisible(true);
		

	}
	
//Analysis Methods 
	public static double getAvgRepTime(ArrayList<sentence> sents){
		double total = 0.0; double num = 0.0; 
		for(int i = 0; i < sents.size(); i++){
			if(sents.get(i).isDescriber && sents.get(i).prev != null){
				total += sents.get(i).getRepTimePrev();
				num++; 
			}
		}
		return total/num; 
	}
	
	public double getAvgRepTime(ArrayList<sentence> sents, double start, double end){
		double total = 0.0; double num = 0.0; 
		for(int i = 0; i < sents.size(); i++){
			sentence s = sents.get(i);
			if(s.isDescriber && s.prev != null && s.start >= start && s.start <= end){
				total += sents.get(i).getRepTimePrev();
				num++; 
			}
		}
		return total/num; 
	}
//Helper Methods
	//Generate output file 
	
	public static void generateOutput(String filename, double start, double end){
		 BufferedWriter writer = null;
	        try {
	            //create a temporary file
	            
	            File logFile = new File(filename);

	            // This will output the full path where the file will be written to...
	            System.out.println(logFile.getCanonicalPath());

	            writer = new BufferedWriter(new FileWriter(logFile));
	            
	            for(int i = 0; i < sents.size(); i++){
	            	sentence s = sents.get(i);
	            	if(s.isDescriber && s.prev != null && s.start >= start && s.start <= end){
	    				writer.write(sents.get(i).getRepTimePrev() + "\n");
	    				
	    			}
	    		}
	        } catch (Exception e) {
	            e.printStackTrace();
	        } finally {
	            try {
	                // Close the writer regardless of what happens...
	                writer.close();
	            } catch (Exception e) {
	            }
	        }
	}
	//Generate Array of intervals from praat file
	public static interval[] toIntervalArray(String fileLocation, boolean isDescriber) throws IOException{
		FileReader reader = new FileReader(fileLocation);
		interval[]intArray; 
		int counter; 
		
		BufferedReader bufRead = new BufferedReader(reader);
		String myLine = null;
		counter = 0; 
		for(int i = 0; i < 13; i++) myLine = bufRead.readLine(); //skip first 14 lines
		
		//Get max xmax
		String[] line = myLine.split(" ");
		double xmaxDesc = Double.parseDouble(line[line.length-1]);
		
		//Create Interval Array
		myLine = bufRead.readLine();
		line = myLine.split(" ");
		int length = Integer.parseInt(line[line.length-1]);
		intArray = new interval[length];
		
		while ( (myLine = bufRead.readLine()) != null){    
			myLine = bufRead.readLine(); //skip "interval [#]
			
			line = myLine.split(" ");
			double xmin = Double.parseDouble(line[line.length - 1]);
			
			myLine = bufRead.readLine();
			line = myLine.split(" ");
			double xmax = Double.parseDouble(line[line.length - 1]);
			
			myLine = bufRead.readLine();
			boolean silent = myLine.contains("silent");
		    
			intArray[counter] = new interval(xmin, xmax, silent, isDescriber);
			
			counter++; 
		}
		return intArray;
	}
	//Get interval for current time
	public static interval getCurrentInt(interval[] int1, double time){
		for(interval i : int1){
			if(!i.isSilent && ((i.xmin <= time) && (i.xmax >= time))){ return i;}
		}
	
		return null; 
	}
	
	//Merge describer and interrogator intervals into single conversation
	public static ArrayList<interval> createConversation(interval[] descInt, interval[] intInt){
		ArrayList<interval> convo = new ArrayList<interval>();
		double time = Math.max(descInt[descInt.length-1].xmax, descInt[descInt.length-1].xmax);
		
		for(double i = 0; i <= time; i += 0.1 ){
			interval curDesc = getCurrentInt(descInt, i);
			interval curInt = getCurrentInt(intInt, i);
			
			if((curDesc != null) && (!convo.contains(curDesc))) convo.add(curDesc); 
			else if ((curInt != null) && (!convo.contains(curInt))) convo.add(curInt);
		}
		
		for(int i = 0; i < convo.size(); i++){
			//Set next
			if(i == convo.size() - 1 ) convo.get(i).next = null;
			else convo.get(i).next = convo.get(i + 1);
			
			//set prev
			if(i == 0) convo.get(i).prev = null; 
			else convo.get(i).prev = convo.get(i - 1);
			
			convo.get(i).convoNum = convo.indexOf(convo.get(i));
		}
		return convo; 
				
	}
//Sentence Methods

	//Retrieves sentence containing inputed interval 
	public static sentence getSentence(interval Int, ArrayList<sentence> sents){
		for(int i = 0; i < sents.size(); i++){
			if(sents.get(i).contains(Int)) return sents.get(i);
		}
		return null;
	}
	
	//Parses conversation into sentences and returns an ordered list of those sentences
	public static ArrayList<sentence> createSentList(ArrayList<interval> convo){
		ArrayList<sentence> sent = new ArrayList<sentence>();
		
		for(int i = 0; i < convo.size(); i++){ //for every interval in the conversation
			if(getSentence(convo.get(i), sent) == null){ //if interval i isn't contained in a sents
				sent.add(new sentence(convo.get(i))); //create it's sentence and add it to sent
			}
		}
		
		for(int i = 0; i < sent.size(); i++){
			//Set next
			if(i == sent.size() - 1 ) sent.get(i).next = null;
			else sent.get(i).next = sent.get(i + 1);
			
			//set prev
			if(i == 0) sent.get(i).prev = null; 
			else sent.get(i).prev = sent.get(i - 1);
			
			
		}
		
		return sent;
	}
	

}
