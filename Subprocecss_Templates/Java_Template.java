//Enter package here
import java.util.*;

class testJava{  
    
    public static String transcribe(String path) {
        String transcript = "Put your transcription function here.";
        return transcript;
    }

    public static void main(String args[]){
        Scanner input = new Scanner(System.in);
        String path = input.nextLine();  
        input.close();
        
        System.out.println(transcribe(path));  
    }  
} 