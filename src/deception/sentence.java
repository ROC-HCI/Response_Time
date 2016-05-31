package deception;

import java.util.ArrayList;

public class sentence extends ArrayList<interval>{
	
	sentence next;
	sentence prev; 
	double start; 
	double end; 
	boolean isDescriber;
	
	
	public sentence(interval i){
		interval temp = i; 
		//If interval is an entire sentence 
		if(((i.next == null) || (i.next.isDescriber != i.isDescriber)) && ((i.prev == null) || (i.prev.isDescriber != i.isDescriber) )){
			this.add(i); 	
		} else{
			//Set temp to first sound in sentence
			while( (temp.prev != null) && (temp.prev.isDescriber == i.isDescriber) ) temp = temp.prev;
		
			//Add sentence intervals to list 
			while((temp != null) && (temp.isDescriber == i.isDescriber) ){
				this.add(temp);
				temp = temp.next;
			}
		}
		
		
		start = getStartTime();
		end = getEndTime();
		isDescriber = this.get(0).isDescriber;
	}
	
	public double getStartTime(){ return this.get(0).xmin;}
	public double getEndTime() {return this.get(this.size()-1).xmax;}
	public boolean isDescriber(){return this.get(0).isDescriber;}
	
	public double getRepTimeNext(){return next.start - end; }
	public double getRepTimePrev(){return start - prev.end;} 
	
	public String toString(){
		String str = "";
		
		for(int i = 0; i < this.size(); i++){
			str += this.get(i) + "\n";
		}
		return str;
	}

}
