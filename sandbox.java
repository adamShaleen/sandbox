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
