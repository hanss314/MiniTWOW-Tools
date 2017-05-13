import random;	

data = []	

void setup() {
	calculateResults(data);					
}						
void calculateResults(String data[][]){						
	Random r = new Random();					
	int[][] results = new int[14][3];					
	for(int ini=0; ini<14; ini++){					
		for(int tia=0; tia<3; tia++){				
			results[ini][tia] = 0;			
		}				
	}
	// 14 is simply the amount of competitors remaining					
	int[] live = new int[10];					
	live[0] = 10;					
	//omitted 1 to 8
	live[9] = 1;
	// for lack of better methods, each array value corresponds to the amount of survivors after each round
	for(int length = 0; length<100; length++){					
		boolean[] dead = new boolean[12];				
		for(int round = 0; round<10; round++){					
			float[] scores = new float[12];			
			for(int sim = 0; sim<12; sim++){			
				if(dead[sim]){		
					scores[sim] = 0;	
				} else {		
					scores[sim] = (float)(r.nextGaussian()*Float.valueOf(data[sim][2])+Float.valueOf(data[sim][1]));					
				}		
			}			
			for(int i = 0; i<12; i++){			
				int rank = 1;		
				for(int j = 0; j<12; j++){		
					if(scores[i] < scores[j]){	
						rank++;
					}	
				}		
				if(rank>live[round]){		
					dead[i] = true;	
				}		
			}
			//the values for round are simply the values for which 10, 3, and 1 people would stay alive			
			if(round==0){			
				for(int ten = 0; ten<12; ten++){		
					if(!dead[ten]){	
						results[ten][0]+=1;
					}	
				}		
			} else if(round==7){			
				for(int three = 0; three<12; three++){		
					if(!dead[three]){	
						results[three][1]+=1;
					}	
				}		
			} else if(round==9){			
				for(int win = 0; win<12; win++){		
					if(!dead[win]){	
						results[win][2]+=1;
					}	
				}		
			}			
		}				
	}					
	for(int prin=0;prin<12;prin++){					
		println(data[prin][0] + "\t" + results[prin][0] + "\t" + results[prin][1] + "\t" + results[prin][2]);				
	}					
}						
			
	# arrays in which the first element is the name as a string, the second the average, and the third the standard deviation