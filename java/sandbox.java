//=============================================================================
// Hacker Rank Java Sort

// class Student {
//     private int id;
//     private String fname;
//     private double cgpa;
//     public Student(int id, String fname, double cgpa) {
//         super();
//         this.id = id;
//         this.fname = fname;
//         this.cgpa = cgpa;
//     }
//     public int getId() {
//         return id;
//     }
//     public String getFname() {
//         return fname;
//     }
//     public double getCgpa() {
//         return cgpa;
//     }
// }
//
// public class Solution {
//     public static void main(String[] args){
//         Scanner scanner = new Scanner(System.in);
//         int testCases = Integer.parseInt(scanner.nextLine());
//
//         List<Student> studentList = new ArrayList<Student>();
//         while (testCases > 0) {
//             int id = scanner.nextInt();
//             String fname = scanner.next();
//             double cgpa = scanner.nextDouble();
//
//             Student student = new Student(id, fname, cgpa);
//             studentList.add(student);
//
//             studentList.sort(Comparator.comparing(Student::getCgpa).reversed().thenComparing(Student::getFname));
//
//             testCases--;
//         }
//
//           for (Student student: studentList){
//             System.out.println(student.getFname());
//         }
//     }
// }

//=============================================================================
// Hacker Rank syntax checker

// import java.util.Scanner;
// import java.util.regex.*;
//
// public class Solution {
// 	public static void main(String[] args) {
//
//         Scanner scanner = new Scanner(System.in);
// 		int numOfTestCases = Integer.parseInt(scanner.nextLine());
//
//         while (numOfTestCases > 0) {
// 			String pattern = scanner.nextLine();
//
//             try {
//                 Pattern.compile(pattern);
//                 System.out.println("Valid");
//             } catch (PatternSyntaxException e) {
//                 System.out.println("Invalid");
//             }
//             numOfTestCases--;
// 		}
// 	}
// }

//=============================================================================
// Hacker Rank String reverse

// import java.io.*;
// import java.util.*;
//
// public class Solution {
//
//     public static void main(String[] args) {
//
//         Scanner scanner = new Scanner(System.in);
//         String str = scanner.next();
//         StringBuilder strBuilder = new StringBuilder(str);
//
//         System.out.println(strBuilder.reverse().toString().equals(str) ? "Yes" : "No");
//     }
// }

//=============================================================================
// Hacker Rank Currency formatter

// import java.io.*;
// import java.util.*;
// import java.text.*;
// import java.math.*;
// import java.util.regex.*;
//
// public class Solution {
//
//     public static void main(String[] args) {
//         Scanner scanner = new Scanner(System.in);
//         double payment = scanner.nextDouble();
//         scanner.close();
//
//         Locale INDIA = new Locale("en", "IN");
//
//         NumberFormat us = NumberFormat.getCurrencyInstance(Locale.US);
//         NumberFormat india = NumberFormat.getCurrencyInstance(INDIA);
//         NumberFormat china = NumberFormat.getCurrencyInstance(Locale.CHINA);
//         NumberFormat france = NumberFormat.getCurrencyInstance(Locale.FRANCE);
//
//         System.out.println("US: " + us.format(payment));
//         System.out.println("India: " + india.format(payment));
//         System.out.println("China: " + china.format(payment));
//         System.out.println("France: " + france.format(payment));
//     }
// }

//=============================================================================
// Hacker Rank Static initializer block

// import java.io.*;
// import java.util.*;
// import java.text.*;
// import java.math.*;
// import java.util.regex.*;
//
// public class Solution {
//
//     public static Scanner scan = new Scanner(System.in);
//     public static int B;
//     public static int H;
//     public static boolean flag = true;
//     static {
//         B = scan.nextInt();
//         H = scan.nextInt();
//         if (B < 0 || H < 0) {
//             flag = false;
//             System.out.println("java.lang.Exception: Breadth and height must be positive");
//         }
//     }
// public static void main(String[] args){
//         if(flag){
//             int area=B*H;
//             System.out.print(area);
//         }
//
//     }//end of main
//
// }//end of class


//=============================================================================
// Hacker Rank End of file

// import java.io.*;
// import java.util.*;
//
// public class Solution {
//
//     public static void main(String[] args) {
//
//         Scanner scan = new Scanner(System.in);
//         int num = 1;
//         while (scan.hasNext()) {
//             System.out.println(num + " " + scan.nextLine());
//             num++;
//         }
//     }
// }

//=============================================================================
// Hacker Rank Data types

// import java.util.*;
// import java.io.*;
//
// class Solution{
//     public static void main(String []argh) {
//
//         Scanner scan = new Scanner(System.in);
//         int TestCases = scan.nextInt();
//
//         for (int i = 0; i < TestCases; i++) {
//
//             try {
//                 long num = scan.nextLong();
//
//                 System.out.println(num + " can be fitted in:");
//                 if (num >= -128 && num <= 127)System.out.println("* byte");
//                 if (num >= -32768 && num <= 32767)System.out.println("* short");
//                 if (num >= -Math.pow(2, 31) && num <= Math.pow(2, 31)-1)System.out.println("* int");
//                 if (num >= -Math.pow(2, 63) && num <= Math.pow(2, 63)-1)System.out.println("* long");
//             }
//             catch (Exception e) {
//                 System.out.println(scan.next()+" can't be fitted anywhere.");
//             }
//
//         }
//     }
// }

//=============================================================================
// Hacker Rank Java Loops 2

// class Solution {
//     public static void main(String []argh) {
//         Scanner in = new Scanner(System.in);
//         int queries = in.nextInt();
//
//         for (int i = 0; i < queries; i++){
//
//             int a = in.nextInt();
//             int b = in.nextInt();
//             int c = in.nextInt();
//
//             for (int y = 0; y < c; y++) {
//                 a += b;
//                 System.out.print(a + " ");
//                 b *= 2;
//             }
//
//             System.out.println();
//         }
//         in.close();
//     }
// }

//=============================================================================
// Hacker Rank Java if/else

// public class Solution {
//
//     private static final Scanner scanner = new Scanner(System.in);
//
//     public static void main(String[] args) {
//         int N = scanner.nextInt();
//         scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");
//
//         boolean isEven = (N % 2 == 0);
//
//         if (!isEven || (isEven && N >= 6 && N <= 20)) {
//             printOutcome(true);
//         } else if ((isEven && N >= 2 && N <= 4) || N > 20) {
//             printOutcome(false);
//         }
//
//         scanner.close();
//     }
//
//     private static void printOutcome(boolean weird) {
//         System.out.println(weird ? "Weird" : "Not Weird");
//     }
// }
