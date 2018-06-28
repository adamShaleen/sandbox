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
