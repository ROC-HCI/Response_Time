package deception;

public class interval {
	double xmin; 
	double xmax; 
	boolean isSilent;
	boolean isDescriber; 
	int convoNum; 
	interval next; 
	interval prev; 
	
	public interval (double xmin, double xmax, boolean silent, boolean isDescriber){
		this.xmin = xmin; 
		this.xmax = xmax; 
		this.isSilent = silent; 
		this.isDescriber = isDescriber; 
	}
	
	public String toString(){
		return "Convo #: " + convoNum + "\nisDescriber: " + isDescriber + "\n" + "xmin: " + xmin + " \n" + "xmax: " + xmax + " \n" + "isSilent: " + isSilent + " \n";  
	}
	
	public int xMin(int mult){return (int) Math.round(xmin*mult);}
	public int xMax(int mult){return (int) Math.round(xmax*mult);}
	
	public int width(int mult){return (int) Math.round((xmax - xmin)*mult); }
	
}
