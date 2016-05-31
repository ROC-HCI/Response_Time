package deception;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.util.ArrayList;

import javax.sound.sampled.*;
import javax.swing.*;



public class plot extends JPanel{
	interval[]descInts; 
	interval[]intInts; 
	ArrayList<interval> convo; 
	ArrayList<sentence> sents;
	int barX; 
	Clip descClip = AudioSystem.getClip();
	Clip intClip = AudioSystem.getClip();
	Timer timer;
	double time;
	JButton pause; 
	JLabel timeLabel, repTime; 
	
	public plot( ArrayList<sentence> sents, interval[] descInts, interval[] intInts, ArrayList<interval> convo,  AudioInputStream descAudio, AudioInputStream intAudio) throws LineUnavailableException, IOException{
		this.descInts = descInts;
		this.intInts = intInts;
		this.convo = convo;
		this.sents = sents;
		barX = 2; 
		time = 0.2; 
		
		//Start Sound Clips
		descClip.open(descAudio);
		intClip.open(intAudio);
		repaint();
		
		
		//Create and start timer
		timer = new Timer(200, new ActionListener(){
			@Override
			public void actionPerformed(ActionEvent e) {
				barX++; 
				time += 0.2;
				timeLabel.setText("Time: " + Math.round(time * 100.0) / 100.0 + "s");
				sentence cur = getCurrentSent(time);
				if((cur != null) && (cur.prev != null))
					repTime.setText("Response Time: " + cur.getRepTimePrev() + "s");
				repaint();
			}
		});
		timer.start();
		
		//Create and add GUI Components 
			
		pause = new JButton("start/stop");
		pause.addActionListener(new ActionListener(){
			@Override
			public void actionPerformed(ActionEvent e) {
				if(timer.isRunning()){
					timer.stop(); descClip.stop(); intClip.stop();
				} else{
					timer.start(); descClip.start(); intClip.start();
				}	
			}});
		add(pause);
		
		timeLabel = new JLabel("Time: " + time + " s");
		add(timeLabel);
		
		repTime = new JLabel("Response Time: " + 0 + " s");
		add(repTime);
	
		//Start sound clips
		descClip.start();
		intClip.start();
			
	}
	
	public void paintComponent(Graphics g){
	
//		//Paint Describer Intervals 
//			for(int i = 0; i < descInts.length; i++){
//				if(!descInts[i].isSilent){
//					paintInterval(g, descInts[i], Color.RED);
//				}
//			}
//			
//		//Paint Interrogator Intervals 	
//		for(int i = 0; i < intInts.length; i++){
//			if(!intInts[i].isSilent){
//				paintInterval(g, intInts[i], Color.BLUE);
//			}
//		}
//		
//		//Paint Current Sentence
//		interval cur = getCurrentInt(time);
//		if(cur != null){
//			ArrayList<interval> sent = new sentence(cur);
//			for(int i = 0; i < sent.size(); i++) paintInterval(g, sent.get(i), Color.GREEN);
//		}
//		System.out.println(cur + "\nConvo #: " + convo.indexOf(cur));
		
	
		
		for(int i = 0; i< sents.size(); i++){
			paintSentence(g, sents.get(i), Color.BLUE, Color.RED);
		}
		
		if(getCurrentSent(time) != null) paintSentence(g, getCurrentSent(time), Color.GREEN, Color.GREEN);
		
		//Line
		g.setColor(Color.RED);
		g.drawLine(barX, this.getHeight(), barX, 0);
			
	}
	
	
	
	
	//Graphical Methods
	public void paintInterval(Graphics g, interval i, Color c ){
		g.setColor(c);
		int yMult;
		if(i.isDescriber) yMult = 3; else yMult = 6; 
		g.fillRect(i.xMin(5), (this.getHeight()/10)*yMult, i.width(5), this.getHeight()/10);
		
	}
	
	public void paintSentence(Graphics g, sentence s, Color intColor, Color descColor){
		if(s.isDescriber()) 
			for(int i = 0; i < s.size(); i++) paintInterval(g, s.get(i), descColor);
		else 
			for(int i = 0; i < s.size(); i++) paintInterval(g, s.get(i), intColor);
			
	}
	
	//Analysis Methods
	
	public interval getCurrentInt(interval[] int1, double time){
		for(interval i : int1){
			if(!i.isSilent && ((i.xmin <= time) && (i.xmax >= time))){ return i;}
		}
	
		return null; 
	}
	
	public interval getCurrentInt(double time){
		interval descCur = getCurrentInt(descInts, time);
		if( descCur!= null) return descCur;
		interval intCur = getCurrentInt(intInts, time);
		if( intCur!= null) return intCur;
		return null;
	}
	
	public static sentence getSentence(interval Int, ArrayList<sentence> sents){
		for(int i = 0; i < sents.size(); i++){
			if(sents.get(i).contains(Int)) return sents.get(i);
		}
		return null;
	}
	
	public sentence getCurrentSent(double time){
		for(int i = 0; i < sents.size(); i++){
			sentence s = sents.get(i);
			if(((s.getStartTime() <= time) && (s.getEndTime() >= time))){ return s;}
		}

		return null; 
	}
	
	
	
	
	
}


