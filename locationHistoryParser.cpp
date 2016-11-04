#include <stdio.h>
#include <vector>
#include <iostream>
#include <algorithm>
#include <string>
#include <fstream>
using namespace std;

string rowDivider="  }, {";
ifstream *mapsFile;
string *column_titles=new string[13];
string *currentLine=new string[13];
string currentItem,previousItem;
int arrayLevel=0;
int DEBUG=0;
string line;

int main(){
	previousItem="";
	for(int i=0;i<14;i++){
		currentLine[i]=",";
	}
	column_titles[0]="timestampMs";
	column_titles[1]="latitudeE7";
	column_titles[2]="longitudeE7";
	column_titles[3]="accuracy";
	column_titles[4]="ActivitysTimestamp";
	column_titles[5]="onFoot";
	column_titles[6]="inVehicle";
	column_titles[7]="onBicycle";
	column_titles[8]="still";
	column_titles[9]="walking";
	column_titles[10]="running";
	column_titles[11]="exitingVehicle";
	column_titles[12]="tilting";
	column_titles[13]="unknown";
	mapsFile.open("LocationHistory.json","r");
	for(int i=0;i<14;i++){
		cout<<column_titles[i];
	}
	cout<<"\n";
	while(mapsFile>>line);			// I'm stuck trying to read the file a line at a time like I did in line 32 of the python script
	
	/*	previousItem=currentItem;
		currentItem=line;
		if(arrayLevel==1){
			//todo
		}
		else if(arrayLevel==2){
			//todo
		}
		else if(arrayLevel==3){
			//todo
		}
		if(currentItem.find("[ {")!=std::string::npos){
			arrayLevel++;
		}
		if(currentItem.find("} ]")!=std::string::npos){
			arrayLevel--;
		}*/
	}
	fclose(mapsFile);
	return 0;
}
