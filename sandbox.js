//---------------Code Wars Too Many Cats----------------------------

// function catPredictor(startDate,endDate) {
//     let start = new Date(startDate);
//     let end = new Date(endDate);
//     let catCount = 0;

//     while (start <= end) {
//       if (start.getDay() != 0) {
//         catCount += 1.15;
//       }
//       start = incrementDate(start);
//     }

//     // Not sure if it's me or the test cases but I thought we needed to round down?
//     return catCount == 22.999999999999993 ? Math.round(catCount) : Math.floor(catCount);
//   }

//   function incrementDate(date) {
//     return new Date(date.setDate(date.getDate() + 1));
//   }

//---------------Code Wars Odd Ones Out-----------------------------

// function oddOnesOut(nums) {
//     return nums.reduce((a, c) => {
//       if (occursEven(getOccurences(nums, c))) {
//         a.push(c)
//       }
//       return a
//     }, [])
//   }

//   function getOccurences(arr, target) {
//     return arr.filter(i => i == target).length;
//   }

//   function occursEven(arrLength) {
//     return (arrLength % 2 == 0) ? true : false;
//   }

//---------------Code Wars Password Validator-----------------------

// Trying to be functional!

// function password(requirements, str) {
//     return requirements.map(f => f(str)).includes(false) ? false : true
//   }

//   function validUpperCase(str) {
//     return Array.isArray(str.match(/[A-Z]/g))
//   }

//   function validLowerCase(str) {
//     return Array.isArray(str.match(/[a-z]/g))
//   }

//   function validNumber(str) {
//     return Array.isArray(str.match(/[0-9]/g))
//   }

//   function validLength(str) {
//     return str.length >= 8
//   }

//   const validation = [validUpperCase, validLowerCase, validNumber, validLength]

//---------------Code Wars Remove Duplicate Words--------------------

// function removeDuplicateWords (s) {
//     return [...new Set(s.split(" "))].join(" ")
//   }

//---------------Code Wars Sum of Array Averages----------------------

// Code Wars test runner wouldn't let me use node 11

// function sumAverage(arr) {
//     const output = arr.map(a => {
//         return (a.reduce((acc, curr) => acc + curr, 0) / a.length);
//     })

//     return Math.floor(output.reduce((a, c) => a + c, 0));
//   }

//---------------Code Wars Chuck Norris IV - Bearded Fist-------------

// function fistBeard(arr) {
//   return [].concat(...arr).reduce((a, c) => {
//     return a + String.fromCharCode(c)
//   }, "")
// }

//---------------Code Wars Well of Ideas - Easy

// function well(x){
//   const goods = x.filter(e => e === "good");
//   return goods.length > 2 ? "I smell a series!" : goods.length > 0 ? "Publish!" : "Fail!"
// }

//---------------Code Wars Grasshopper-Grade Book----------------------

// function getGrade(s1, s2, s3) {
//   const averageScore = getAverageScore(s1, s2, s3);
//   return getLetterGrade(averageScore);
// }

// function getAverageScore(s1, s2, s3) {
//   return (s1 + s2 + s3) / 3;
// }

// function getLetterGrade(score) {
//   return score >= 90 ?
//     "A"
//     :
//     score >= 80 && score < 90 ?
//     "B"
//     :
//     score >= 70 && score < 80 ?
//     "C"
//     :
//     score >= 60 && score < 70 ?
//     "D"
//     :
//     "F"
// }

//---------------Code Wars Playing with Sets Sup:Sub-------------------

// function isSubsetOf(s1, s2){
//   const arr = [];
//   s1.forEach(i => arr.push(s2.has(i)))
//   return arr.includes(false) ? false : true
// }

// function isSupersetOf(s1, s2){
//   const arr = [];
//   s2.forEach(i => arr.push(s1.has(i)))
//   return arr.includes(false) ? false : true
// }

//---------------Code Wars Find Maximum and Minimum Values of a List----

// function max(arr) {
//   return sortArr(arr)[arr.length -1]
// }

// function min(arr) {
//   return sortArr(arr)[0]
// }

// function sortArr(arr) {
//   return arr.sort((a, b) => a - b)
// }

//---------------Code Wars Sort out the Men from the Boys----------

// function menFromBoys(arr){
//   const even = []
//   const odd = []

//   arr.map(i => isEven(i) ? even.push(i) : odd.push(i))

//   const evenSet = removeDuplicate(even)
//   const oddSet = removeDuplicate(odd)

//   evenSet.sort((a, b) => a - b)
//   oddSet.sort((a, b) => b - a)

//   return evenSet.concat(oddSet)
// }

// function isEven(int) {
//   return int % 2 === 0
// }

// function removeDuplicate(arr) {
//   return [...new Set(arr)]
// }

//---------------Code Wars Sum of Cubes----------------------------

// function sumCubes(n) {
//   return getRange(n).reduce((a, c) => {
//     return (cube(c)) + a
//   }, 0)
// }

// function getRange(n) {
//   return Array(n).fill(1).map((x, y) => x + y)
// }

// function cube(n) {
//   return n * n * n
// }

//---------------Code Wars Sum of Odd Cubed Numbers----------------

// function cubeOdd(arr) {
//   if (containsInvalid(arr)) return undefined
//   return arr.reduce((a, c) => {
//     return isOdd(c) ? cube(c) + a : a
//   }, 0)
// }

// function cube(int) {
//   return int * int * int
// }

// function isOdd(int) {
//   return int % 2 !== 0
// }

// function containsInvalid(arr) {
//   return arr.filter(i => !Number.isInteger(i)).length > 0
// }

//---------------Code Wars Count the smiley faces------------------

// function countSmileys(arr) {
//   return arr.reduce((a, c) => {
//     const charArr = c.split("");
//     if (hasNose(charArr)) {
//       if (isValidEyes(charArr[0]) && isValidNose(charArr[1]) && isValidMouth(charArr[2])) {
//         a++
//       }
//     } else {
//       if (isValidEyes(charArr[0]) && isValidMouth(charArr[1])) {
//         a++
//       }
//     }
//     return a
//   }, 0)
// }

// function hasNose(arr) {
//   return arr.length === 3
// }

// function isValidEyes(char) {
//   return char === ":" || char === ";"
// }

// function isValidNose(char) {
//   return char === "-" || char === "~"
// }

// function isValidMouth(char) {
//   return char === ")" || char === "D"
// }

//---------------Code Wars Maximum Multiple------------------------

// function maxMultiple(divisor, bound) {
//   let largestInt = 0
//   const range = createRange(divisor, bound)

//   range.map(int => {
//     if (isLargest(divisor, bound, largestInt, int)) {
//       largestInt = int
//     }
//   })
//   return largestInt
// }

// function isLargest(divisor, bound, currentLargest, int) {
//   return (Number.isInteger(int / divisor) && int <= bound && int > 0 && int > currentLargest)
// }

// function createRange(start, stop) {
//   const output = []
//   for (let i = start; i <= stop; i++) {
//     output.push(i)
//   }
//   return output;
// }

//---------------Code Wars Maximum Triplet Sum---------------------

// function maxTriSum(numbers) {
//   const formattedArr = [...new Set(numbers)].sort((a, b) => b - a)
//   return formattedArr.slice(0, 3).reduce((a, c) => a + c, 0)
// }

//---------------Code Wars Row Weights-----------------------------

// Definitely not in love with this version

// function rowWeights(arr) {
//   const team1 = [0];
//   const team2 = [0];

//   arr.map((person, i) => {
//     if (isEven(i)) {
//       team1.push(arr[i]);
//     } else {
//       team2.push(arr[i]);
//     }
//   })

//   const team1Output = combineWeights(team1);
//   const team2Output = combineWeights(team2);

//   return [team1Output, team2Output];
// }

// function combineWeights(arr) {
//   return arr.reduce((a, c) => a + c, 0);
// }

// function isEven(index) {
//   return index % 2 === 0;
// }

//---------------Code Wars Word Values------------------------------

// this one was harder than it should have been

// const alphaMap = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9,
//   "j": 10, "k": 11, "l": 12, "m": 13, "n": 14, "o": 15, "p": 16, "q": 17, "r": 18, "s": 19,
//   "t": 20, "u": 21, "v": 22, "w": 23, "x": 24, "y": 25, "z": 26}

// function wordValue(arr) {
//   return arr.map((str, i) => {
//     const position = i + 1
//     return str.replace(/[^a-z0-9]/g, "").split("").reduce((a, c) => {
//       return a + alphaMap[c]
//     }, 0) * position
//   })
// }

//---------------Code Wars My Languages-----------------------------

// const myLanguages = (results) => {

//   return Object.entries(results)
//     .filter(result => result[1] > 59)
//     .sort((a, b) => b[1] - a[1])
//     .map(result => result[0]);
// }

//---------------Code Wars Lottery Ticket---------------------------

// const bingo = (ticket, win) => {

//   let miniWinCount = 0;

//   ticket.map((currentTicket, index) => {
//     if (currentTicket[0].includes(String.fromCharCode(currentTicket[1]))) {
//       miniWinCount++;
//     }
//   })

//   return (miniWinCount >= win ? 'Winner!' : 'Loser!');
// }

//---------------Code Wars Coding Meetup #2-------------------------
// example of creating a copy of an array of objects, adding a new property, and not mutating the original by using the spread operator

// function greetDevelopers(list) {
//   return list.map(index =>
//     index = {...index, greeting: `Hi ${index.firstName}, what do you like the most about ${index.language}?`
//   });
// }

//----------------FizzBuzz-------------------------------------------

// Yes, you've done this one a bunch, but here's a different take on it while using a ternary across all conditions

// fizzBuzz = () => {

//   for (let i = 1; i < 101; i++) {
//   	console.log((i % 15 === 0 ? "FizzBuzz" :
//     		i % 3 === 0 ? "Fizz" :
//     		i % 5 === 0 ? "Buzz" :
//     		i));
// 	}
// }

//----------------Code Wars 'Round by 0.5 steps'----------------------

// function solution(n){
//   let numArr = n.toString().split('.');
//   let wholeNum = parseInt(numArr[0]);
//   let numToEvaluate = '0.' + numArr[1];
//
//   if (numToEvaluate < .3) {
//     return Math.round(n);
//   }
//
//   else if (numToEvaluate > .25 && numToEvaluate < .75) {
//     return wholeNum + .5;
//   }
//
//   else if (numToEvaluate >= .75) {
//     return wholeNum + 1;
//   }
// }

//----------------Free Code Camp 'Pairwise'----------------------------

// function pairwise(arr, arg) {
//
//   var indicies = [];
//
//   function indexObject(index) {
//     this.index = index;
//     this.hasBeenUsed = false;
//   }
//
//   var output = [];
//
//   for (var i = 0; i < arr.length; i++) {
// 		indicies.push(new indexObject(i));
//     for (var y = 0; y < arr.length; y++) {
//       indicies.push(new indexObject(y));
// 			if (arr[i] + arr[y] === arg && !indicies[i].hasBeenUsed && !indicies[y].hasBeenUsed && arr.indexOf(i) !== arr.indexOf(y)) {
//       	output.push(i + y);
//         indicies[i].hasBeenUsed = true;
//         indicies[y].hasBeenUsed = true;
//       }
//     }
//   }
//
//   if (output.length === 0) {
//     return 0;
//   }
//
//   return output.reduce(function(a, b) {return a + b;});
// }
//
// pairwise([1,4,2,3,0,5], 7);

//-----------------Free Code Camp 'Map the Debris'----------------------

// function orbitalPeriod(arr) {
//
//   var GM = 398600.4418;
//   var earthRadius = 6367.4447;
//   var output = [];
//
//   for (var index in arr) {
//   	output.push({name: arr[index].name, orbitalPeriod: Math.round(2 * Math.PI * Math.sqrt( (earthRadius + arr[index].avgAlt) ** 3 / GM))})
//   }
//
//   return output;
// }
//
// orbitalPeriod([{name : "sputnik", avgAlt : 35873.5553}]);

//-----------------Free Code Camp 'Make A Person'------------------------

// var Person = function(firstAndLast) {
//
//   var fullName = firstAndLast;
//
//   this.getFirstName = function() {
//   	return fullName.split(" ")[0];
//   };
//
//   this.getLastName = function() {
// 	return fullName.split(" ")[1];
//   };
//
//   this.getFullName = function() {
//   	return fullName;
//   };
//
//   this.setFirstName = function(first) {
// 	fullName = first + " " + fullName.split(" ")[1];
//   };
//
//   this.setLastName = function(last) {
// 	fullName = fullName.split(" ")[0] + " " + last;
//   };
//
//   this.setFullName = function(name) {
//   	fullName = name;
//   };
// };

//------------------Code Wars Detect Pangram----------------------------

// A pangram is a sentence that contains every single letter of the alphabet at least once. For example, the sentence "The quick brown fox jumps over the lazy dog" is a pangram, because it uses the letters A-Z at least once (case is irrelevant).
// Given a string, detect whether or not it is a pangram. Return True if it is, False if not. Ignore numbers and punctuation.

// function isPangram(string){

//   // create an alphabetical array to checkoff characters that are found
//   var alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];

//   // convert the string passed in to a sorted array of lowercase characters with any non-alphabetical character removed
//   var stringSplitToArray = string.toLowerCase().replace(new RegExp(/([^a-zA-Z\d\+])/, 'g'), '').split('').sort();

//   // check each character of the string array to determine if it has an alphabetical character, and if so remove (check off) that character
//   for (var i = 0; i < stringSplitToArray.length; i++) {
//     if (alphabet.includes(stringSplitToArray[i])) {
//       alphabet.shift();
//     }
//   }

//   // if all the characters have been removed, then the sentence does contain all alphabetical characters
//   if (!alphabet.length > 0) {
//     return true;
//   }

//   // if not all of the characters are removed, it doesn't contain all alphabetical characters
//   return false;
// }

//------------------Code Wars Sum of Odd Numbers------------------------

// Given the triangle of consecutive odd numbers:

//              1
//           3     5
//        7     9    11
//    13    15    17    19
// 21    23    25    27    29
// ...
// Calculate the row sums of this triangle from the row index (starting at index 1) e.g.:

// rowSumOddNumbers(1); // 1
// rowSumOddNumbers(2); // 3 + 5 = 8

// function rowSumOddNumbers(row) {
//     return row * row * row;
// }

//------------------Free Code Camp "No Repeats Please"------------------------

// function permAlone(str) {
//
//   var allPermutations = permutator(str.split(''));
//   var output = [];
//
//   // another loop to remove any permutation with a duplicate from the array
//   for (var i = 0; i < allPermutations.length; i++) {
//   	if (!hasRepeatingCharacter(allPermutations[i])) {
//       output.push(allPermutations[i]);
//     }
//   }
//
//   // return the length of array
//   return output.length;
// }
//
// function permutator(inputArr) {
//   var results = [];
//
//   function permute(arr, memo) {
//     var cur, memo = memo || [];
//
//     for (var i = 0; i < arr.length; i++) {
//       cur = arr.splice(i, 1);
//       if (arr.length === 0) {
//         results.push(memo.concat(cur));
//       }
//       permute(arr.slice(), memo.concat(cur));
//       arr.splice(i, 0, cur[0]);
//     }
//
//     return results;
//   }
//
//   return permute(inputArr);
// }
//
// function hasRepeatingCharacter(arr) {
//
//   var testString = 0;
//
//   for (var i = 0; i < arr.length; i++) {
//   	testString = testString + arr[i];
//   }
//
//   return (/(\w)\1+/.test(testString));
// }
//
// permAlone('aab');

//------------------Recursion Factorial Practice-------------------------------

// function factorialByIteration(num) {
//
// 	let current = num;
//   for (i = current; i > 0; i--) {
//   	if (i !== 1) {
//     	current = current * (i-1);
//     }
//   }
//
//   return current;
// }
//
// function factorialByRecursion(num) {
//
//   if (num === 1) {
//   	return 1;
//   }
//
//   return num * factorialByRecursion(num - 1);
// }

//------------------Free Code Camp "Inventory Update"--------------------------

// function updateInventory(arr1, arr2) {

//   for (i = 0; i < arr1.length; i++) {
//     for (y = 0; y < arr2.length; y++) {	// loop through both arrays
//       if (arr1[i][1] == arr2[y][1]) {
//         arr1[i][0] += arr2[y][0];		// if item is same, update qty in arr1
//         arr2.splice(y, 1);			// if item is same, remove item from arr2
//       }
//     }
//   }

//   arr1 = arr1.concat(arr2);			// combine the remaining items of both arrays

//   arr1 = arr1.sort(function(a, b) {  // return alphabetically sorted array
//     var outputA = removeHyphen(a[1]);
//     var outputB = removeHyphen(b[1]);
//     return ( ( outputA == outputB ) ? 0 : ( ( outputA > outputB ) ? 1 : -1 ) );
//   });

//   return arr1;
// }

// function removeHyphen(string) {
// 	return string.replace("-", " ");
// }

// // Example inventory lists
// var curInv = [
//     [21, "Bowling Ball"],
//     [2, "Dirty Sock"],
//     [1, "Hair Pin"],
//     [5, "Microphone"]
// ];

// var newInv = [
//     [2, "Hair Pin"],
//     [3, "Half-Eaten Apple"],
//     [67, "Bowling Ball"],
//     [7, "Toothpaste"]
// ];

// updateInventory(curInv, newInv);

//-------------------Reduce Method---------------------------------------------

// Sum indexes of array
// var arr = [1, 2, 3];
// var output1 = arr.reduce((a, b) => a + b);
// console.log(output1);
//
// // Flatten an array (Turn an array of arrays into a single)
// var arrOfArrays = [[1], [2], [3]];
// var output2 = arrOfArrays.reduce((a, b) => a.concat(b));
// console.log(output2);

//-------------------Free Code Camp "Exact Change"-----------------------------

// // Create an object which hold the denominations and their values
// var money = [
//   {name: 'ONE HUNDRED', val: 100.00},
//   {name: 'TWENTY', val: 20.00},
//   {name: 'TEN', val: 10.00},
//   {name: 'FIVE', val: 5.00},
//   {name: 'ONE', val: 1.00},
//   {name: 'QUARTER', val: 0.25},
//   {name: 'DIME', val: 0.10},
//   {name: 'NICKEL', val: 0.05},
//   {name: 'PENNY', val: 0.01}
// ];
//
// function checkCashRegister(price, payment, drawer) {
//   var change = payment - price;
//
//   // Transform Drawer array into object
//   var register = drawer.reduce(function(a, b) {
//     a.total += b[1];
//     a[b[0]] = b[1];
//     return a;
//   }, {total: 0});
//
//   // Handle exact change
//   if (register.total === change) {
//     return 'Closed';
//   }
//
//   // Handle obvious insufficent funds
//   if (register.total < change) {
//     return 'Insufficient Funds';
//   }
//
//   // Loop through the denomination array
//   var change_arr = money.reduce(function(a, b) {
//     var value = 0;
//     // While there is still money of this type in the drawer
//     // And while the denomination is larger than the change reminaing
//     while (register[b.name] > 0 && change >= b.val) {
//       change -= b.val;
//       register[b.name] -= b.val;
//       value += b.val;
//
//       // Round change to the nearest hundreth deals with precision errors
//       change = Math.round(change * 100) / 100;
//     }
//     // Add this denomination to the output only if any was used.
//     if (value > 0) {
//         a.push([ b.name, value ]);
//     }
//     return a; // Return the current Change Array
//   }, []); // Initial value of empty array for reduce
//
//   // If there are no elements in change_arr or we have leftover change, return
//   // the string "Insufficient Funds"
//   if (change_arr.length < 1 || change > 0) {
//     return "Insufficient Funds";
//   }
//
//   // Here is your change, ma'am.
//   return change_arr;
// }
//
// console.log(checkCashRegister(19.50, 20.00, [["PENNY", 1.01], ["NICKEL", 2.05],
// ["DIME", 3.10], ["QUARTER", 4.25], ["ONE", 90.00], ["FIVE", 55.00], ["TEN", 20.00],
// ["TWENTY", 60.00], ["ONE HUNDRED", 100.00]]));  //[["QUARTER", 0.50]]

//-------------------Free Code Camp 'Symmetric Difference'---------------------

// function sym(args) {
//
//   let argsArray = [].slice.call(arguments);
//
//   function difference(arr1, arr2) {
//
//     let unique = [];
//
//     for (let i = 0; i < arr1.length; i++) {
//     	if (arr2.indexOf(arr1[i]) < 0 && unique.indexOf(arr1[i]) < 0) {
//       	unique.push(arr1[i]);
//       }
//     }
//
//     arr2.forEach(function(item) {
//       if (arr1.indexOf(item) < 0 && unique.indexOf(item) < 0) {
//       	unique.push(item);
//       }
//     });
//
//     return unique;
//   }
//
//   return argsArray.reduce(difference);
// }
//
// sym([1, 2, 3], [5, 2, 1, 4]);

//-------------------Free Code Camp 'Validate US Telephone Numbers'------------

// function telephoneCheck(num) {
//
//   var regExp = /^(\+|1\s?)?(\([0-9]{3}\)\s?|[0-9]{3}\-?|[0-9]{3}\s?)([0-9]{3}\-?|[0-9]{3}\s?)[0-9]{4}$/;
//
//   if (num.match(regExp)) {
//     return true;
//   }
//
//   return false;
// }
//
// telephoneCheck("555-555-5555");

//-------------------Free Code Camp 'Arguments Optional'-----------------------

//This is the example from the forum.  Spent 2 days and couldn't come up with anything that worked by myself :(

// function addTogether() {
//
//   function isNum(num) {
//     if (typeof num !== 'number') {
//       return undefined;
//     } else
//       return num;
//   };
//
//   if (arguments.length > 1) {
//     var a = isNum(arguments[0]);
//     var b = isNum(arguments[1]);
//     if (a === undefined || b === undefined) {
//       return undefined;
//     } else {
//       return a + b;
//     }
//   } else {
//
//     var c = arguments[0];
//     if (isNum(c)) {
//       return function(arg2) {
//         if (c === undefined || isNum(arg2) === undefined) {
//           return undefined;
//         } else {
//           return c + arg2;
//         }
//       };
//     }
//   }
// }
//
// console.log(addTogether(2, 5)); // 7
// console.log(addTogether(2)(3)); // 5
// console.log(addTogether(2, "3")); // undefined
// console.log(addTogether(2)([3])); // undefined

//-------------------Free Code Camp 'Everything Be True'--------------------------

// function truthCheck(collection, pre) {
//
//   for (let i = 0; i < collection.length; i++) {
//     if (!collection[i][pre]) {
//     	return false;
//     }
//   }
//
//   return true;
// }
//
// console.log(truthCheck([{"user": "Tinky-Winky", "sex": "male"},
// {"user": "Dipsy", "sex": "male"}, {"user": "Laa-Laa", "sex": "female"},
// {"user": "Po", "sex": "female"}], "sex"));  // true

//-------------------Free Code Camp 'Binary Agents'-------------------------------

// function binaryAgent(str) {
//
//   // convert the full string into an array of just the binary values
//   let arr = str.split(" ");
//
//   // placeholder value
//   let num = [];
//
//   // loop through arr of binary strings
//   for (let i = 0; i < arr.length; i++) {
//
//use base param from parseInt and convert to Character value
// 		num.push(String.fromCharCode(parseInt(arr[i], 2)));
//   }
//
//   // concatinate the array of character strings into a sentence
//   return num.join("");
// }
//
// console.log(binaryAgent("01000001 01110010 01100101 01101110
//00100111 01110100 00100000 01100010 01101111 01101110 01100110
//01101001 01110010 01100101 01110011 00100000 01100110 01110101
//01101110 00100001 00111111"));  // Aren't bonfires fun!?

//-------------------Free Code Camp 'Steamroller'----------------------------------

// function steamrollArray(arr) {

//   // create a new array to put the values of all the nested business
// 	let output = [];

// 	// helper function to determine if need to go another level deeper to get to the actual value
// 	function flatten(arg) {
//   	if (!Array.isArray(arg)) {
//     	output.push(arg);
//     } else {
//     	for (let x in arg) {
//       	flatten(arg[x]);
//       }
//     }
//   }

//   // for every element in the array run the helper function and then return the final outcome
//   arr.forEach(flatten)
//   	return output;
// }

//-------------------Free Code Camp 'Drop it'---------------------------------------

// function dropElements(arr, func) {
//
//   // if the array is not empty and the first index doesn't pass the function
//   while (arr.length > 0 && !func(arr[0])) {
//
//   	// remove it from the array
//   	arr.shift();
//   }
//
//   // return whatever is left
//   return arr;
// }

//-------------------Free Code Camp 'Finders Keepers'--------------------------------

// function findElement(arr, func) {
//
//   for (let i = 0; i < arr.length; i++) {
//   	if (func(arr[i])) {
//     	return arr[i];
//     }
//   }
// }

//-------------------Free Code Camp 'Smallest Common Multiple'-----------------------

// function smallestCommons(arr) {
//
//   // sort the argument array largest to smallest and initialize an empty array for the range
//   arr = arr.sort(function(a, b) { return b-a;});
//   let range = [];
//
// 	// add the range of numbers from the argument array to the range array
//   for (let i = arr[0]; i >= arr[1]; i--) {
//   	range.push(i);
//   }
//
//   // set the lcm to the first range array element and loop through testing for the GCD
//   let lcm = range[0];
//   for (let y = 1; y < range.length; y++) {
//   	let GCD = gcd(lcm, range[y]);
//     lcm = (lcm * range[y]) / GCD;
//   }
//
//   return lcm;
//
//   // Euclidean algorithm helper function.  Drastically reduces the amount of loops
//   function gcd(x, y) {
//   	if (y === 0) {
//     	return x;
//     } else {
//     	return gcd(y, x%y);
//     }
//   }
//
// }

//-------------------Free Code Camp 'Sum Primes'--------------------------------------

// function isPrime(value) {                // helper function to determine if num is prime
//
//     for (let i = 2; i < value; i++) {
// 			if (value % i === 0) {
//       	return false;
//       }
//     }
//     return value > 1;
//   }
//
//
// function sumPrimes(num) {
//
//   let primeSum = 0;
//
//   for (let y = 0; y <= num; y++) {
// 		if (isPrime(y)) {
//     	primeSum = primeSum + y;
//     }
//   }
//
//   return primeSum;
// }
//
// console.log(sumPrimes(10)); // 17
// console.log(sumPrimes(977)); // 73156

//--------------------Free Code Camp 'Sum all odd fibonacci numbers'--------------------

// function sumFibs(num) {
//
//   let fibNum = [1, 1];	// always starts with 1 and 1
//   for (let i = 2; i <= num;) {
//       fibNum.push(i);
//       i = fibNum[fibNum.length - 1] + fibNum[fibNum.length - 2];  // adds the last 2 numbers pushed together
//   }
//
//   let output = fibNum.reduce(function(a, b) {	// remove all even numbers from array and return the sum
//       if (b % 2 !== 0) {
//       	return a + b;
//       } else {
//       	return a;
//       }
//   });
//
//   return output;
// }
//
// console.log(sumFibs(4));  // 5
// console.log(sumFibs(20)); // 25

//--------------------Free Code Camp 'Spinal Tap Case'--------------------

// function spinalCase(str) {
//
//   // puts a space before any encountered upper case, set everythig to lower case, replaces spaces and _ with -
// 	return str.replace(/([a-z])([A-Z])/g, '$1 $2').toLowerCase().split(/(?:_| )+/).join("-");
//
// }

//--------------------Free Code Camp 'Convert HTML entities'--------------------

// function convertHTML(str) {
//
// 	const testCases = {
//     '&':'&amp;',
//     '<':'&lt;',
//     '>':'&gt;',
//     '\"':'&quot;',
//     '\'':"&apos;"
//   };
//
// 	for (let i = 0; i < str.length; i++) {
//   	if (testCases.hasOwnProperty(str[i])) {
//     	str = str.replace(str[i], testCases[str[i]]);
//     }
//   }
//
//   return str;
// }
//
// console.log(convertHTML("Dolce & Gabbana"));  // Dolce &amp; Gabbana

//--------------------Free Code Camp 'Sorted Union'--------------------

// function uniteUnique(arr) {
//
// 	let output = [];
//
//   for (let i = 0; i < arguments.length; i++) {
//   	output.push(arguments[i]);
//   }
//
//   output = output.reduce(function(a, b) { return a.concat(b);}, []);
//
//   return output.filter(function(num, index) {
//     return output.indexOf(num) === index;
// 	})
// }
//
// console.log(uniteUnique([1, 3, 2], [5, 2, 1, 4], [2, 1]));  // [1, 3, 2, 5, 4]

//--------------------Free Code Camp 'Boo who'--------------------

// function booWho(bool) {
//
// 	if (typeof(bool) === 'boolean') {
//   	return true ;
//   }
//
//   return false;
//
// }
//
// console.log(booWho(null));  // false
// console.log(booWho(false)); // true
// console.log(booWho([1, 2, 3])); // false
// console.log(booWho([].slice)); // false
// console.log(booWho({ "a": 1 })); //  false
// console.log(booWho(1)); //  false
// console.log(booWho(NaN)); //  false
// console.log(booWho("a")); //  false
// console.log(booWho("true")); //  false
// console.log(booWho("false")); // false

//--------------------Codewars 'Missing Letters'--------------------

// function fearNotLetter(str) {
//   // loop through string
//   for (let i = 0; i < str.length; i++) {
//   	// create local variable to hold char code value of i
//     let code = str.charCodeAt(i);
//     // if the next character isn't sequential
//     if (code !== str.charCodeAt(0) + i) {
//     	// return what character that would have been
//       return String.fromCharCode(code - 1);
//     }
//
// 	}
//   // otherwise return undefined
//   return undefined;``
// }
//
// console.log(fearNotLetter("abce"));  // d
// console.log(fearNotLetter("abcdefghjklmno")); // i
// console.log(fearNotLetter("bcd")); // undefined

//--------------------Codewars 'Zebulans Nightmare'--------------------

// function toCamelCase(str) {
//
//     let arr = str.split('');
//
//     for (let i = 0; i < arr.length; i++) {
// 		if (arr[i] === '_') {
//     	    arr.splice(i, 1);
//          arr[i] = arr[i].toUpperCase();
//         }
//     }
//
//     return arr.join('');
// }
//
// console.log(toCamelCase("taco_bowl")); // tacoBowl
// console.log(toCamelCase("taco_party_bowl"));  // tacoPartyBowl

//--------------------Free Code Camp 'DNA Pairing'--------------------

// function pairElement(str) {
//   //define a map object with all pair possibilities
//   var map = {T:'A', A:'T', G:'C', C:'G'};
//   //split str into a char Array
//   strArr = str.split('');
//   //replace each Array item with a 2d Array using map
//   for (var i=0;i<strArr.length;i++){
//     strArr[i]=[strArr[i], map[strArr[i]]];
//   }
//  return strArr;
// }

// not my solution^^^

// // helper function
// function getBasePair(str) {
//     if (str === "A") { return "T";}
//     if (str === "T") { return "A";}
//     if (str === "C") { return "G";}
//     if (str === "G") { return "C";}
//   }
//
// function pairElement(str) {
//
//   var output = [];
//
//   for (let i = 0; i < str.length; i++) {
// 		var arr = [str[i], getBasePair(str[i])];
//     output.push(arr);
//   }
//
//   return output;
// }
//
// console.log(pairElement("ATCGA")); // [["A","T"],["T","A"],["C","G"],["G","C"],["A","T"]
// console.log(pairElement("TTGAG")); // [["T","A"],["T","A"],["G","C"],["A","T"],["G","C"]]
// console.log(pairElement("CTCTA")); // [["C","G"],["T","A"],["C","G"],["T","A"],["A","T"]]

//--------------------Timeout closures example with ES6--------------------

// function closures(arr) {
// 	for (let i = 0; i < arr.length; i++) {
//   // using the ES6 let syntax, it creates a new binding
//   // every single time the function is called
//   	setTimeout(function() {
//     	console.log('The index of this number is: ' + i);
//   	}, 1000);
// 	}
// }

//-------------------Free Code Camp 'Pig Latin'---------------------------

// function translatePigLatin(str) {
//
//   var vowels = ["a", "e", "i", "o", "u"];
//   var arr = str.split('');
//
//   	if (vowels.indexOf(arr[0]) !== -1 && vowels.indexOf(arr[1]) !== -1 || vowels.indexOf(arr[0]) !== -1 && vowels.indexOf(arr[1]) === -1) {
//     	return str + 'way';
//     }
//
//     else if (vowels.indexOf(arr[0]) === -1 && vowels.indexOf(arr[1]) === -1) {
//     	return str.substr(2) + str[0] + str[1] + 'ay';
//     }
//
//       else if (vowels.indexOf(arr[0]) === -1 && vowels.indexOf(arr[1]) !== -1) {
//     		return str.substr(1) + str[0] + 'ay';
//     	}
// }
//
// console.log(translatePigLatin("california")); // aliforniacay
// console.log(translatePigLatin("paragraphs")); // aragraphspay
// console.log(translatePigLatin("glove")); // oveglay
// console.log(translatePigLatin("algorithm")); // algorithmway
// console.log(translatePigLatin("eight")); // eightway

//-------------------Free Code Camp 'Search and replace'---------------------------

// function myReplace(str, before, after) {
//
// 	if (before.split('')[0] === before.split('')[0].toUpperCase()) {
//   	  after = after.split('');
//       after = after[0].toUpperCase() + after.splice(1,after.length).join('');
//     }
//
// 	return str.replace(before, after);
// }
//
// myReplace("A quick brown fox jumped over the lazy dog", "jumped", "leaped");

//-------------------Free Code Camp 'Wherefore art thou'---------------------------

// function whatIsInAName(collection, source) {
//
//   var sourceKeys = Object.keys(source);
//
//   return collection.filter(function(object) {
//     for (var i = 0; i < sourceKeys.length; i++) {
//       if (object[sourceKeys[i]] == source[sourceKeys[i]]) {
//         var result = true;
//       } else {
//         result = false;
//       }
//     }
//     return result;
//   });
//
// }
//
// console.log(whatIsInAName([{ "a": 1, "b": 2 }, { "a": 1 }, { "a": 1, "b": 2, "c": 2 }], { "a": 1, "b": 2 }));
//
// console.log(whatIsInAName([{ first: "Romeo", last: "Montague" }, { first: "Mercutio", last: null }, { first: "Tybalt", last: "Capulet" }], { last: "Capulet" }));
//
// console.log(whatIsInAName([{ "a": 1, "b": 2 }, { "a": 1 }, { "a": 1, "b": 2, "c": 2 }], { "a": 1, "c": 2 }));

//-------------------Free Code Camp 'Roman Numeral Converter'---------------------------

// function convertToRoman(num) {
//
//   var output = "";
//   var standard = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1];
//   var roman = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I'];
//
//   for (var i = 0; i < standard.length; i++) {
//     while (num >= standard[i]) {
//       output += roman[i];
//       num -= standard[i];
//     }
//   }
//
//   return output;
// }
//
// console.log(convertToRoman(2));
// console.log(convertToRoman(36));
// console.log(convertToRoman(1450));

//-------------------Free Code Camp 'Diff Two Arrays'---------------------------

// function diffArray(arr1, arr2) {
//
// var output = [];
//
// // if the element in arr1 is not in arr2 and not in output, push to output
// arr1.forEach(function(element) {
// 	if (arr2.indexOf(element) < 0 && output.indexOf(element) < 0) {
//   	output.push(element);
//   }
// });
//
// // if the element in arr2 is not in arr1 and not in output, push to output
// arr2.forEach(function(element) {
// 	if (arr1.indexOf(element) < 0 && output.indexOf(element) < 0) {
//   	output.push(element);
//   }
// });
//
// return output;
//
// }
//
//
// console.log(diffArray(['taco', 'taco', 'burrito'], ['taco', 'taco', 'taco'])); //['burrito']

//-------------------Free Code Camp 'Sum All Numbers in a Range'---------------------------

// function sumAll(arr) {
//   var output = [];
// 	arr = arr.sort(function(a, b) { return a - b;});
// 	for (var i = arr[0]; i <= arr[1]; i++) {
//   	output.push(i);
//   }
//   return output.reduce(function(a, b) { return a + b; }, 0);
// }
//
//
// console.log(sumAll([1, 4]));  // 10
// console.log(sumAll([4, 1]));  // 10
// console.log(sumAll([5, 10])); // 45
// console.log(sumAll([10, 5])); // 45

//-------------------Codewars 'Printer Errors'---------------------------------------------

// function printerError(s) {
//     return s.match(/[^a-m]/g).length + "/" + s.length;
// }

// console.log(printerError("aaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbmmmmmmmmmmmmmmmmmmmxyz"));  // 3/56

//-------------------Free Code Camp 'Ceasars Cipher'---------------------------------------------

// function rot13(str) {
//   let conversion = [];
//   for (let i = 0; i < str.length; i++) {
//   	conversion.push(str.charCodeAt(i));
//   }
//     for (let j = 0; j < conversion.length; j++) {
//   	  if (conversion[j] > 64 && conversion[j] <= 77) {
//     	  conversion[j] += 13;
//       } else if (conversion[j] > 77) {
//     	  conversion[j] -= 13;
//       }
//     }
//       for (let k = 0; k < conversion.length; k++) {
//   	    conversion[k] = String.fromCharCode(conversion[k]);
//       }
//   return conversion.join('');
// }

//-------------------codewars 'array.diff'-------------------------------------------------------

//It should remove all values from list a, which are present in list b.
//difference([1,2],[1]) == [2]
//If a value is present in b, all of its occurrences must be removed from the other:
//difference([1,2,2,2,3],[2]) == [1,3]

// function array_diff(a, b) {
//   return a.filter(function (item) {
//     return b.indexOf(item) < 0;
//   });
// }

//-------------------codewars 'Word Search'-------------------------------------------------------

// function wordSearch(target, arr){
// 	let output = [];
//   for (let i = 0; i < arr.length; i++) {
//   	if (arr[i].toLowerCase().indexOf(target.toLowerCase()) !== -1) {
//     	output.push(arr[i]);
//     }
//   }
//   if (output.length === 0) {
//   	return ["Empty"];
//   } else {
//   	return output;
//   }
// }

//-------------------codewars 'Find the odd int'-------------------------------------------------------

// function oddInt(arr) {
//   let x;
//   for (let i = 0; i < arr.length; i++) {
//     x = x^arr[i];
//   }
//   return x;
// }

//------------------------------------------------------------------------------------------------------
// baby's first ternary

// function shit(num) {
// 	let output;
// 	num % 2 === 0 ? output = "even" : output = "odd";
//   return output;
// }

//-------------------------------------------------------------------------------------------------------
//  Codewars 'Two fighters, one winner'

// function Fighter(name, health, damagePerAttack) {
//         this.name = name;
//         this.health = health;
//         this.damagePerAttack = damagePerAttack;
// }

// function declareWinner(fighter1, fighter2, firstAttacker) {
// 	while (fighter1.health > 0 && fighter2.health > 0) {
//   	if (fighter1.name === firstAttacker) {
//     	fighter2.health = fighter2.health - fighter1.damagePerAttack;
//       if (fighter2.health > 0) {
//       	fighter1.health = fighter1.health - fighter2.damagePerAttack;
//       }
//     }
//     else {
//     	fighter1.health = fighter1.health - fighter2.damagePerAttack;
//       if (fighter1.health > 0) {
//       	fighter2.health = fighter2.health - fighter1.damagePerAttack;
//       }
//     }
//   }
//   if (fighter1.health <= 0) {
//   	return fighter2.name;
//   }
//   else {
//   	return fighter1.name;
//   }
// }

// console.log(declareWinner(new Fighter("Lew", 10, 2), new Fighter("Harry", 5, 4), 'Lew'));  // Lew
// console.log(declareWinner(new Fighter("Harald", 20, 5), new Fighter("Harry", 5, 4), 'Harry'));  // Harry
// console.log(declareWinner(new Fighter("Harald", 20, 5), new Fighter("Harry", 5, 4), "Harry"));  // Harald
// console.log(declareWinner(new Fighter("Jerry", 30, 3), new Fighter("Harald", 20, 5), "Jerry"));  // Harald

//----------------------------------------------------------------------------------------------------------------------

// Codewars 'Money, Money, Money' Kata 8
// ES6 (sort of).  Really really ugly way of doing this.

// function calculateYears(principal, interest, tax, desired) {

//   let years = 0;
//   let interestGained = 0;
//   let subtractTax = 0;
//   let totalToAdd = 0;

//     if (principal === desired) {
//       return years;
//     }

//     while (principal < desired) {
// 			interestGained = (principal * interest);	// 50
// 			subtractTax = (interestGained * tax);  //  9
//       totalToAdd = interestGained - subtractTax;
//       principal += totalToAdd;
//       years++;
//     }

//     return years;
// }

// console.log(calculateYears(1000, .05, .18, 1100));  // 3
// console.log(calculateYears(1000,0.01625,0.18,1200));  // 14
// console.log(calculateYears(1000,0.05,0.18,1000));  // 0

// create a clone of an object with a new property
// still getting an error on codewars
// twin must reflect changes to original
// twin must reflect new properties added to orginal
// function evilTwin(object) {
// 	var twin = {hasGoatee: true};
// 	for (var key in object) {
// 		twin[key] = object[key];
// 	}
// 	return twin;
// }

//-------------------------------------------------------------------------------------------------------
// Free Code camp
// Where do I belong

// function getIndexToIns(arr, num) {
// 	arr.push(arguments[1]);
//   var newArr = arr.sort(function(a, b){return a-b});
//   for(var i = 0; i < newArr.length; i++) {
// 		if (newArr[i] === arguments[1]) {
// 			return i;
//     }
//   }
// }

//---------------------------------------------------------------------------------------------------------
//Free Code camp
//Seek and destroy

// function destroyer(arr) {
//   for(var i=arr.length -1; i>=0; i--){
//   	for(var j=0; j<arguments.length; j++) {
// 			if (arr[i] === arguments[j]) {
//       	arr.splice(i, 1);
//       }
//     }
//   }
//   return arr;
// }
//
// destroyer([1, 2, 3, 1, 2, 3], 2, 3);

//---------------------------------------------------------------------------------------------------------
//Free Code camp
//Falsey Bouncer

// function bouncer(arr) {
// 	for (var i = arr.length -1; i >= 0; i--) {
//   	if (Boolean(arr[i]) !== true) {
//     	arr.splice(i, 1);
//     }
//   }
//   return arr;
// }
//
// console.log(bouncer([7, "ate", "", false, 9]));  // [7, 'ate', 9]
// console.log(bouncer([false, null, 0, NaN, undefined, ""])); // []

//---------------------------------------------------------------------------------------------------------
//Free Code camp
// 'Mutations' I got the spoiler answer from the forum after struggling for a week

// function mutation(arr) {
//   for (var i = 0; i < arr[1].length; i++){
//     if (arr[0].toLowerCase().indexOf(arr[1][i].toLowerCase()) === -1)
//       return false;
//   }
//   return true;
// }
//
// console.log(mutation(['hello', 'hey']));
// console.log(mutation(['hello', 'Hello']));
// console.log(mutation(["zyxwvutsrqponmlkjihgfedcba", "qrstu"]));

//Another method using ES6
//function mutation(arr) {
//   const first = arr[0].toLowerCase();
//   const second = arr[1].toLowerCase().split('');
//   return second.reduce( (a, b) => a && first.indexOf(b) !== -1, true);
// }

//---------------------------------------------------------------------------------------------------------
//Free Code camp
// 'Slasher Flick'

// function slasher(arr, howMany) {
// 	var cut = arr.splice(0, howMany);
// 	return arr;
// }

//---------------------------------------------------------------------------------------------------------
//Free Code camp
// 'Chunky Monkey'

// function chunkArrayInGroups(arr, size) {
// 	var output = [];
// 	for (var i = arr.length -1; i >= 0; i--) {
// 		if (arr.length) {
// 			output.push(arr.splice(0, size));
// 		}
// 	}
// 	return output;
// }

//---------------------------------------------------------------------------------------------------------
//Free Code camp
// 'Truncate a string'

// function truncateString(str, num) {
// 	if (str.length > num && num <= 3) {
// 		return str.slice(0, num) + '...';
// 	}
// 	else if (str.length > num) {
// 		return str.slice(0, num -3) + '...';
// 	}
// 	return str.slice(0, num);
// }

//---------------------------------------------------------------------------------------------------------
//Free Code camp
// "confirm the ending" without using the endsWith() method

// function confirmEnding(str, target) {
// 	var strLength = target.length;
// 	if(str.substr(-strLength) === target) {
// 		return true;
// 	}
// 	return false;
// }
//
// confirmEnding('He has to give me a new name', 'name');  //true

//---------------------------------------------------------------------------------------------------------
//Code Wars 'Highest and Lowest'

// function highAndLow(numbers) {
// 	var compare - numbers.split(' ').sort(function(a,b){return a-b});
// 	var lowest = compare.splice(0, 1);
// 	var highest = compare.splice(compare.length -1, 1);
// 	if (highest.length === 0) {
// 		return lowest + ' ' + lowest;
// 	}
// 	return highest + ' ' + lowest;
// }

//---------------------------------------------------------------------------------------------------------
//Code Wars 'Exes and Ohs'  super ugly and inefficent
// function XO(str) {
// 	var convert = str.toLowerCase();
// 	var output = convert.replace(/[abcdefghijklmnpqrstuvwyz]/gi, '');
// 	var x = [];
// 	var o = [];
// 	for (var i = 0; i < output.length; i++) {
// 		if (output[i] === 'x') {
// 			x.push(output[i]);
// 		}
// 		else if (output[i] === 'o') {
// 			o.push(output[i]);
// 		}
// 	}
// 	if (x.length === o.length) {
// 		return true;
// 	}
// 	return false;
// }

//---------------------------------------------------------------------------------------------------------
//Code Wars 'Remove the minimum' doesn't use .sort()

// function removeSmallest(arr) {
// 	var min = Math.min.apply(null, arr);
// 	arr.splice(arr.indexOf(min), 1);
// 	return arr;
// }

//---------------------------------------------------------------------------------------------------------
//Code Wars 'Regex validate PIN code'

// function validatePIN(pin) {
// 	var output = pin.replace(/[^0-9]/gi, '');
// 	if (output.length === pin.length && output.length === 4 || output.length === 6) {
// 		return true;
// 	}
// 	return false;
// }

//---------------------------------------------------------------------------------------------------------
//Code Wars 'Highest profit'
// It's not pretty...

// function minMax(arr) {
// 	var min = 100;
//   var max = -1000000;
//   for (var i = arr.length -1; i >= 0; i--) {
//   	if (arr[i] < min) {
//     	min = arr[i];
//     }
//     if (arr[i] > max) {
//     	max = arr[i];
//     }
//   }
//   return [min, max];
// }

//---------------------------------------------------------------------------------------------------------
//Code Wars 'Reverse Words'

// function reverseWords(str) {
// 	var output = str.split(' ');
// 	for (var i = 0; i < output.length; i++) {
// 		output[i] = output[i].split('').reverse().join('');
// 	}
// 	return output.join(' ');
// }
//
// reverseWords('This is an example!');

//---------------------------------------------------------------------------------------------------------
//Code Wars 'Tea for two'

// function tea42(input) {
// 	var output = input.toString().split('');
// 	for (var i = 0; i < input.length; i++) {
// 		if (output[i] === 2 || output[i] === '2') {
// 			output.splice(i, 1, 't');
// 		}
// 	}
// 	return output;
// }
//
// tea42('pre2ty');  => pretty

//---------------------------------------------------------------------------------------------------------
//Free code camp
// Return largest numbers from each array of numbrs in an array

// function largestNums(array) {
// 	var largest = [];
// 	for (var i = 0; i < array.length; i++) {
// 		array[i].sort(function(a, b){return b-a;});
// 		largest.push(array[i][0]);
// 	}
// 	return largest;
// }
//
// largestNums([4, 5, 1, 3], [13, 27, 18, 26], [32, 35, 37, 39], [1000, 1001, 857, 1]);  => [5, 27, 39, 1001]

//---------------------------------------------------------------------------------------------------------
//Free code camp
// Capitalize first letter of every word in a string, rest of letters are lowercase

// function titleCase(str) {
// 	var array = str.toLowerCase().split(' ');
// 	for (var i = 0; i < array.length; i++) {
// 		var cap = array[i].charAt(0).toUpperCase();
// 		array[i] = cap + array[i].substr(1);
// 	}
// 	return array;
// }
//
// titleCase("I'm a little teapot"); => "I'm A Little Teapot"

//---------------------------------------------------------------------------------------------------------
//Free code camp
//Return length(number) of the longest word in a string

// function findLongestWord(string) {
//   var longest = 0;
//   var array = string.split(' ');
//   for (var i = array.length -1; i >= 0; i--) {
//     if (array[i].length > longest) {
//         longest = array[i].length;
//     }
//   }
//   return longest;
// }
//
// console.log(findLongestWord('I like tacos')); => 5

//---------------------------------------------------------------------------------------------------------
//Free code camp
// determine whether a string is a palindrome or not (same forwards and backwards)

// function palindrome(string) {
// 	var forward = string.replace(/[^A-Za-z0-9]/g, '');
// 	var backward = forward.split('').reverse().join('');
// 		if (forward === backward) {
// 			return true;
// 		}
// 		return false;
// }
//
// palindrome('eye');  => true
// palindrome('fart'); => false

//----------------------------------------------------------------------------------------------------------------
//Factorialize a single number
// function factorialize(num) {
// 	var output = 1;
// 	for (var i = 1; i <= num; i++) {
// 		output = output * i;
// 	}
// 	return output;
// }
//
// factorialize(5); => 120
// factorialize(10); => 3628800

//----------------------------------------------------------------------------------------------------------------
//Remove all duplicate instances from an array

// function removeDuplicates(array) {
// 	var sorted = array.sort();
// 	for (var i = array.length; i > 0; i--) {
// 		if (sorted[i] === sorted[i+1]) {
// 			array.splice(i, 1);
// 		}
// 	}
// 	return sorted;
// }

//----------------------------------------------------------------------------------------------------------------
// profile lookup from freecodecamp
// The function should check if firstName is an actual contact's firstName
//and the given property (prop) is a property of that contact.
// If both are true, then return the "value" of that property.
// If firstName does not correspond to any contacts then return "No such contact"
// If prop does not correspond to any valid properties then return "No such property"

// var contacts = [{"firstName": "Akira","lastName": "Laine","number": "0543236543","likes": ["Pizza", "Coding", "Brownie Points"]},
//     			{"firstName": "Harry","lastName": "Potter", "number": "0994372684","likes": ["Hogwarts", "Magic", "Hagrid"]},
//     			{"firstName": "Sherlock","lastName": "Holmes","number": "0487345643","likes": ["Intriguing Cases", "Violin"]},
//     			{"firstName": "Kristian","lastName": "Vos","number": "unknown","likes": ["Javascript", "Gaming", "Foxes"]}];
//
// function lookUpProfile(firstName, prop){
// 	for (var i = contacts.length - 1; i >= 0; i--) {
// 		if (contacts[i].firstName === firstName) {
//     	if (contacts[i].hasOwnProperty(prop)) {
//       	return contacts[i][prop];
//       }
//     	else {
//       	return 'No such property';
//       }
//     }
//   }
//   return 'No such contact';
// }

//----------------------------------------------------------------------------------------------------------------
// filter odd numbers out of an array of numbers

// function filterOutOdd(array) {
// 	return array.filter(function(input) {
// 		return input % 2 === 0 ;
// 	});
// }

//----------------------------------------------------------------------------------------------------------------
//really stupid example of reformatting an object to read in plain english

// function format(object) {
// 	var output = '';
// 	for (var key in object) {
// 		output += key + ' = ' + pairs[key] + ' ,';
// 	}
// 	output = output.slice(0, -2);
// 	return output;
// }

//----------------------------------------------------------------------------------------------------------------
//removing all strings from an array

// function filterOutStrings(array) {
// 	for (var i = array.length -1; i >= 0; i--) {  // loop through backwards to get every instance
// 		if (typeof(array[i]) === 'string') {
// 			array.splice(i, 1);
// 		}
// 	}
// 	return array;
// }

//----------------------------------------------------------------------------------------------------------------
// Your online store likes to give out coupons for special occasions. Some customers try to cheat the system by entering invalid codes or using expired coupons.
//Your mission:
// Write a function called checkCoupon to verify that a coupon is valid and not expired. If the coupon is good, return true. Otherwise, return false.
// A coupon expires at the END of the expiration date. All dates will be passed in as strings in this format: "June 15, 2014"

// function checkCoupon(enteredCode, correctCode, currentDate, expirationDate) {
// 	var current = Date.parse(currentDate);
// 	var exp = Date.parse(expirationDate);
// 	if (enteredCode === correctCode && current <= exp) {
// 		return true;
// 	}
// 	else {
// 		return false;
// 	}
// }

//----------------------------------------------------------------------------------------------------------------
// Given an array of numbers, find the largest pair sum in the array.
// For example
// [10,14,2,23,19] should return 42 (i.e. sum of 23,19)
// [99,2,2,23,19] should return 122 (i.e. sum of 99,23)
// Input array contains minimum two elements and every element is a number.

// So far this works for positive integers only
// function largestPairSum(numbers){
// 	var largestPair = 0;
//   for (var i = 0; i < numbers.length; i++) {
//   	for (var j = 0; j < numbers.length; j++) {
//     	if (numbers[i] + numbers[j] > largestPair && numbers[i] !== numbers[j]) {
//       	largestPair = numbers[i] + numbers[j];
//       }
//     }
//   }
//   return largestPair;
// }
//
// console.log(largestPairSum([10,14,2,23,19]));
// console.log(largestPairSum([99,2,2,23,19]));
// console.log(largestPairSum([-10, -8, -16, -18, -19]));

//----------------------------------------------------------------------------------------------------------------
//Create a function, getVillainName, that returns a villain name based on the user's birthday.
//(The birthday will be passed to the function as a valid Date object, so for simplicity,
//there's no need to worry about converting strings to dates.)The first name will come
//from the month, and the last name will come from the last digit of the date.

// function getVillainName(birthday) {
//
// var firstPosition = birthday.getMonth();
// var lastPosition = birthday.getDate().toString().charAt(1);
// var first = ['Evil', 'Vile', 'Cruel', 'Trashy', 'Despicable', 'Embarrassing', 'Disreputable', 'Atrocious', 'Twirling', 'Orange', 'Terrifying', 'Awkward'];
// var last = [' Mustache', ' Pickle', ' Hood Ornament', ' Raisin', ' Recycling Bin', ' Potato', ' Tomato', ' House Cat', ' Teaspoon', ' Laundry Basket'];
//
// return 'The ' + first[firstPosition] + ' ' + last[lastPosition];
// }

//----------------------------------------------------------------------------------------------------------------
// REGULAR EXPRESSIONS
// Removing lowercase vowels from string

// function shortcut(string) {
//   return string.replace(/[aeiou]/gi, '');
// }

//----------------------------------------------------------------------------------------------------------------
// Calorie Tracker App  CLOSURES

// function calorieTracker(baselineCalories) {
//     // keep track of totalCalories today
//     var totalCaloriesToday = 0;
//     var totalDays = 1;
//     // keep track of totalCalories all time
//     var totalCaloriesAllTime = 0;
//     // keep track of personalBaseLineCalories
//       //in parameter
//     //addCalories()
//     function reportEating(totalCaloriesConsumed) {
//         totalCaloriesToday += totalCaloriesConsumed;
//     }
//     //startNewDay()
//     function startNewDay() {
//         totalCaloriesAllTime += totalCaloriesToday;
//         totalCaloriesToday = 0;
//     }
//     //estimated weight loss today()
//     function getTodaysWeightLoss() {
//         //3500 calories = 1 lb
//         return totalCaloriesToday - baselineCalories / 3500;
//     }
//     //estimated weight loss all time()
//     function getAllTimeWeightLoss() {
//         //3500 calories = 1 lb
//         //today - baseline / 3500
//         return (totalCaloriesToday - (baselineCalories * totalDays)) / 3500;
//     }
//
//     return {
//         reportEating: reportEating,
//         startNewDay: startNewDay,
//         getTodaysWeightLoss: getTodaysWeightLoss,
//         getAllTimeWeightLoss: getAllTimeWeightLoss
//     }
// }
//
// var juansTracker = calorieTracker(2300);
// var pingsTracker = calorieTracker(1800);
// var sumoTracker = calorieTracker(8500);
//
// juansTracker.reportEating(3000);
// juansTracker.startNewDay();
// juansTracker.reportEating(2400);
//
// console.log(juansTracker.getTodaysWeightLoss());
// console.log(juansTracker.getAllTimeWeightLoss());
//
// sumoTracker.reportEating(12000);
// sumoTracker.startNewDay();
// sumoTracker.reportEating(18000);
//
// console.log(sumoTracker.getTodaysWeightLoss());
// console.log(sumoTracker.getAllTimeWeightLoss());
//-----------------------------------------------------------------------------------------------------------

//Factory example  CLOSURES

// function colorFactoryFactory(colorName) {
//     return function paintCanMaker() {
//         console.log('here is a ' + colorName + ' paint can.')
//     }
//     return paintCanMaker;
// }
//
// var redPaintCanFactory = colorFactoryFactory('red');
// var bluePaintCanFactory = colorFactoryFactory('blue');
// var greenPaintCanFactory = colorFactoryFactory('green');
//
// redPaintCanFactory();
// bluePaintCanFactory();
// greenPaintCanFactory();
//-----------------------------------------------------------------------------------------------------------

//Closures  simple example
// function closureFn(num) {
//   var car = 'honda';
//     return function() {
//       console.log('i have a owned ' + num + ' ' + car + "'s!");
//     };
// }
//
// var runTheClosure = closureFn(5);
//
// console.log(runTheClosure());  //I have owned 5 honda's!

//the inner function maintains the vars of the outer function and the gloabal scope
//------------------------------------------------------------------------------------------------------------

// OBJECT.KEY method

// var adam = {
//   name: 'adam',
//   age: 32,
//   height: '5 foot 10'
// }
//
// var ObjectPropertyNames = Object.keys(adam);
//
// console.log(ObjectPropertyNames);
//-----------------------------------------------------------------------------------------------------------

// Objects.  Complex example (bands)

// var bands = [
//   {
//     name: "Joe",
//     email: "Joe@Icansingreallyhigh.com",
//     artist: "Queen"
//   },
//   {
//     artist: "LedZepplin",
//     email: "DeadMepplin@gmail.com",
//     name: "Dead Mepplin"
//   },
//   {
//     artist: "DavidBowie",
//     name: "Johnny Depp",
//     email: "Imnotreallyhim@johnnydeppfan.com"
//   },
//   {
//     name: "Joe",
//     email: "Joe@Icansingreallyhigh.com",
//     artist: "Queen"
//   },
//   {
//     artist: "LedZepplin",
//     email: "DeadMepplin@gmail.com",
//     name: "Dead Mepplin"
//   },
//   {
//     artist: "DavidBowie",
//     name: "Johnny Depp",
//     email: "Imnotreallyhim@johnnydeppfan.com"
//   },
//   {
//     name: "Joey",
//     email: "Joe@Icansingreallyhigh.com",
//     artist: "BritneySpears"
//   },
//   {
//     artist: "LedZepplin",
//     email: "DeadMepplin@gmail.com",
//     name: "Dead Mepplin"
//   },
//   {
//     artist: "DavidBowie",
//     name: "Johnny Mepp",
//     email: "Imnotreallyhim@johnnydeppfan.com"
//   },
//    {
//     artist: "DavidBowie",
//     name: "Johnny Gepp",
//     email: "Imnotreallyhim@johnnydeppfan.com"
//   },
//    {
//     artist: "DavidBowie",
//     name: "Johnny Smepp",
//     email: "Imnotreallyhim@johnnydeppfan.com"
//   }
// ];
//
// function countCoverBands(coverRequests){
//   /*
//     var bands = {}
//
//     var artist
//     var artistCoutn
//
//     for coverRequests
//       increment artistCount
//
//
//     return bands
//   */
//
//   var bands = {}
//
//   for(var i = 0; i < coverRequests.length; i++){
//     var request = coverRequests[i];
//
//     if(bands.hasOwnProperty(request.artist)){
//         bands[request.artist] += 1;
//     } else {
//         bands[request.artist] = 1;
//     }
//   }
//
//   return bands;
// }
//
// var totalResults = countCoverBands(bands);
//
// console.log("total", totalResults)
//
//
// function countCoverBands2(coverRequests){
//   var bands = []
//
//   for(var i = 0; i < coverRequests.length; i++){
//     var request = coverRequests[i];
//
//     var existingBand = null;
//     for(var j = 0; j < bands.length; j++){
//         if(bands[j].artist === request.artist){
//             existingBand = bands[j];
//             break;
//         }
//     }
//
//     if(existingBand){
//         existingBand.count += 1;
//     } else {
//         bands.push({
//             artist: request.artist,
//             count: 1
//         });
//     }
//   }
//
//   return bands;
// }
//------------------------------------------------------------------------------------------------------

//Prototype  simple example
//
// String.prototype.mrT = function() {                 //prototype = shared function
//   return 'I pity the fool that says ' + this;
// }
//
// var soccer = 'I like soccer';
//
// var soccer2 = soccer.mrT();
//
// console.log(soccer2);
//------------------------------------------------------------------------------------------------------

//Callback  simple example

// function adder(num1, num2) {
//   return num1 + num2;
// }
//
// function subtractor(num1, num2) {
//   return num1 - num2;
// }
//
// function calculate(num1, num2, callback) {
//   return callback(num1, num2);
// }
//
// console.log(calculate(2, 3, adder));
// console.log(calculate(3, 2, subtractor));
//-----------------------------------------------------------------------------------------------------

//Callback  simple  array

// Write a function called 'contains', that will have 3 parameters:
// array, name, and a callback function. Have the contains function
// check to see if the name is in the array, if true invoke the callback
// function while passing in true, and return the result, or if not, invoke
// the callback function while passing in false and return the outcome.
//
// var names = ['Cahlan', 'Jeremy', 'Colt', 'Jeff', 'Tyler', 'Ben'];
//
// var foundUser = false;
//
//
// // Create the contains function here
// function contains(array, name, callback) {
//     if (array.indexOf(name) >= 0) {
//       return callback(true);
//     }
//       return callback(false);
// }
//
// contains(names, 'Colt', function(result){
//     if(result === true){
//         foundUser = true;
//         console.log('its true!');
//     } else {
//         foundUser = false ;
//         console.log('its false');
//     }
//   return foundUser;
// });
//---------------------------------------------------------------------------------------

//Callback  in depth example

// First, setup the generic poem creator function; it will be the callback function
//in the getUserInput function below.

// function genericPoemMaker(name, gender) {
//     console.log(name + " is finer than fine wine.");
//     console.log("Altruistic and noble for the modern time.");
//     console.log("Always admirably adorned with the latest style.");
//     console.log("A " + gender + " of unfortunate tragedies who still manages a perpetual smile");
// }
//
// //The callback, which is the last item in the parameter, will be our genericPoemMaker
// //function we defined above.
//
// function getUserInput(firstName, lastName, gender, callback) {
//     var fullName = firstName + " " + lastName;
//
//     // Make sure the callback is a function
//
//     if (typeof callback === "function") {
//
//     // Execute the callback function and pass the parameters to it
//
//     callback(fullName, gender);
//     }
// }
//
// getUserInput("Michael", "Fassbender", "Man", genericPoemMaker);
// // Output
// /* Michael Fassbender is finer than fine wine.
// Altruistic and noble for the modern time.
// Always admirably adorned with the latest style.
// A Man of unfortunate tragedies who still manages a perpetual smile.
// */
//-----------------------------------------------------------------------------------------------------

// Factorial function
// function factorial(num) {
//
//     if (num < 0) {
//         return -1;
//     }
//       else if (num == 0) {
//         return 1;
//       }
//       var tmp = num;
//       while (num-- > 2) {
//         tmp *= num;
//       }
//         return tmp;
// }
//
// console.log(factorial(3));
//----------------------------------------------------------------------------------------------------

// Exponent function

//Create a function called exponent that takes in two parameters, the first parameter
//should represent a number to be multiplied against itself and the second parameter
//should represent how many times it is multiplied by itself. The function should return the
//result of this operation. exponent(2,3) should return 8

// function exponent(multNum, timesNum) {
//   var newNum = multNum;
//   for (var i = 2; i <= timesNum; i++) {
//     newNum = newNum * multNum;
//   }
//   return newNum;
// }
//
// console.log(exponent(2, 3));
// console.log(exponent(2, 2));
//----------------------------------------------------------------------------------------------------

// Even number finder (array function)

// Create a function called evenFinder that takes an array as an argument
//and returns an array with all of the odd numbers removed.

// var testArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
//
// function evenFinder(array) {
//   for (var i = array.length - 1; i >= 0; i--) {
//     if (array[i] % 2 !== 0) {
//       array.splice(i, 1)
//     }
//   }
//   return array;
// }
//
// console.log(evenFinder(testArray));
//---------------------------------------------------------------------------------------------------

// Array manipulation (Grocery Function)

//Write a function called removeItem that is given two arguments, the first is an array called
//myGroceryList, and the second is an item to remove from myGroceryList. If the second argument
//(the item to remove) matches an item in myGroceryList, remove that item from your grocery list
//and return the new, updated grocery list.

// var myGroceryList = ['tacos', 'pizza', 'hotdogs', 'banana'];
//
//
//  function removeItem(myGroceryList, itemToRemove) {
//   for (var i = 0; i < myGroceryList.length; i++) {
//     if (myGroceryList[i] === itemToRemove) {
//       myGroceryList.splice(i, 1);
//     }
//   }
//   return myGroceryList;
// }
//
//
// //Once you do that, write another function called addItem that is given two arguments,
//the first is myGroceryList and the second is an item to add to your grocery list. If the item
//is already in the grocery list, do not add it a second time. If it's not in the list, then add it
//and return the new list.
//
//   function addItem(myGroceryList, itemToAdd) {
//       if (myGroceryList.indexOf(itemToAdd) === -1) {
//         myGroceryList.push(itemToAdd);
//     }
//     return myGroceryList;
//   }
//
//   console.log(removeItem(myGroceryList, 'pizza'));
//   console.log(addItem(myGroceryList, 'banana'));
//---------------------------------------------------------------------------------------------------------

//Find in array function

// Write a function called 'findInArray' that takes in two parameters,
//the first representing the array to be searched and the second representing
//the value to be searched for. Return true if the value exists in the array. If it doesn't exist return false.

// var myArray = [1, 2, 3, 4, 5];
//
//
// function findInArray(searchArray, searchValue) {
//   for (var i = 0; i < searchArray.length; i++) {
//     if (searchArray[i] === searchValue) {
//       return true;
//     }
//   }
//   return false;
// }
//
// console.log(findInArray(myArray, 8));
//--------------------------------------------------------------------------------------------------------

// Adjusting array indexes by different amounts.  ReverseLOOPER

// var array = [1,2,3,4,5,6,7,8,9,10,11,12,13];
// function reversedLooper(array) {
//     var newArray = [];
//     var n = -3;
//     for (var i = array.length - 1; i >= 0; i--) {
//       n++;
//         if (array[i] === array.length) {
//             newArray.push(array[i] - 2);
//         }
//         else if (array[i] === array.length - 1) {
//             newArray.push(array[i] - 1);
//         }
//         else if (array[i] === array.length - 2) {
//             newArray.push(array[i]);
//         }
//         else {
//             newArray.push(array[i] + n)
//         }
//     }
//     return newArray;
// }
// console.log(reversedLooper(array));
//-----------------------------------------------------------------------------------------------------

// Array and Object manipulation

/*A very clean way to pass around large LISTS (arrays) of COLLECTIONS (objects)
of Data is to have an Array full of objects. */

//Create an empty array called users.

//Code Here

// var users = [];

/*Now add three user objects to your users array. Each user object should contain the
following properties. name, email, password, username.*/

//include this as one of the objects in your array.
// var user1 = {
//     name: 'Tyler McGinnis',
//     email: 'tylermcginnis33@gmail.com',
//     password: 'iLoveJavaScript',
//     username: 'infiniateLoop'
// };
//
// //Your Code Here
//
// users.user1 = user1;
// users.user2 = {
//     name: 'adam',
//     email: 'adamemail',
//     password: 'adampass',
//     username: 'adamuser'
// };
// users.user3 = {
//     name: 'jen',
//     email: 'jenemail',
//     password: 'jenpass',
//     username: 'jenuser'
// };
//
// /*Now you have a very common data structure. Twitter is a good use case.
// It's easy to imagine that your followers list on Twitter is an Array full or objects
// and those objects contain properties about the specific person you follow.*/
//
// /*Now let's say that Tyler decided to delete his account. Loop through your array of
// objects until you find Tyler's account (use tylermcginnis33@gmail.com to find him).
// Once you find the particular index he's located in, delete him from the array.*/
//
//   //Code Here
//
//   for (var i = 0; i < users.length; i++) {
//   if (users[i].email === 'tylermcginnis33@gmail.com') {
//     users.splice(i, 1);
//   }
// }
//
// //The activity we just did is very much how data works in 'the real world'.
//-------------------------------------------------------------------------------------------------

//Array manipulation with nested for loops

// var num1 = Math.floor(Math.random() * (30 - 0) + 0);
// var num2 = Math.floor(Math.random() * (30 - 0) + 0);
// var arr1 = [];
// var arr2 = [];
// for(var i = 0; i < num1; i++){
//   arr1.push(i);
// }
// for(var i = 0; i < num2; i++){
//   arr2.push(i);
// }
//
// function both(arr1, arr2) {
//   var newArray = [];
//   for (var i = 0; i < arr1.length; i++) {
//     for (var j = 0; j < arr2.length; j++) {
//       if (arr1[i] === arr2[j]) {
//         newArray.push(arr1[i]);
//       }
//     }
//   }
//   return newArray;
// }
//
// console.log(both(arr1, arr2));
//------------------------------------------------------------------------------------------------

//Number function (doing math on an array of mixed 'number' elements)

// var numbers = [5, '9', 16, 19, '25', '34', 48];
// //Write a function called addTen that is given 'numbers' as it's only argument and returns a new
// //array after adding ten to each item in numbers. *Verify your answer is correct. --> [15, 19, 26, 29, 35, 44, 58]
//
// function addTen(numbers) {
//   for (var i = 0; i < numbers.length; i++) {
//     numbers[i] = Number(numbers[i]) + 10;
//   }
//   return numbers;
// }
//
// console.log(addTen(numbers));
//------------------------------------------------------------------------------------------------

//Reverse Function

//Write a function called reverse that takes a given str as it's only argument
//and returns that string after it's been reversed

// function reverseString(string) {
//   return string.split('').reverse().join('');
// }
//
// console.log(reverseString('adam is super cool'));
//------------------------------------------------------------------------------------------------

//  Arrange array in even/odd order and return

// var nums = [1,2,34,54,55,34,32,11,19,17,54,66,13];
//
// function divider(numbersArray) {
//   var even = [];
//   var odd = [];
//   var newArray = [];
//   for (var i = 0; i < numbersArray.length; i++) {
//     if (numbersArray[i] % 2 === 0) {
//       even.push(numbersArray[i]);
//     }
//     else {
//       odd.push(numbersArray[i]);
//     }
//   }
//   newArray[0] = even;
//   newArray[1] = odd;
//   return newArray;
// }
//
// console.log(divider(nums));
//------------------------------------------------------------------------------------------------

// Compare number of string/array characters

// function exOh(str) {
//   var arrayX = [];
//   var arrayO = [];
//   for (var i = 0; i < str.length; i++) {
//     if (str.charAt(i) === 'x') {
//       arrayX.push(str.charAt(i));
//     }
//     else if (str.charAt(i) === 'o') {
//       arrayO.push(str.charAt(i));
//     }
//   }
//       if (arrayX.length === arrayO.length) {
//         return true;
//       }
//       else {
//         return false;
//       }
// }
//
// console.log(exOh('xoxoxoo'));
//--------------------------------------------------------------------------------------------------

// Longest Word Function

// function longestWord(string) {
//     var str = string.split(" ");
//     var longest = 0;
//     var word = null;
//     for (var i = 0; i < str.length; i++) {
//         if (longest < str[i].length) {
//             longest = str[i].length;
//             word = str[i];
//         }
//     }
//     return word;
// }
//
// console.log(longestWord('the longest word is'));

//--------------------------------------------------------------------------------------------------

// Alphabetical order function
//
// function alphabet(str){
//
//  return str.split('').sort().join('')
//
// }
//
// console.log(alphabet('hello'));

//------------------------------------------------------------------------------------------------

// Capitalize all vowels in string Function

// function capVowels(str) {
//
// var newString = '' + str;
//
//   for (var i = 0; i < str.length; i++) {
//
//     if (str.charAt(i) === 'a' || str.charAt(i) === 'e' || str.charAt(i) === 'i' || str.charAt(i) === 'o' || str.charAt(i) === 'u') {
//
//       newString = newString.replace(str.charAt(i), str.charAt(i).toUpperCase());
//
//     }
//
//   }
//
//      return newString;
//
// }
//
// console.log(capVowels('adam is cool.'));

//----------------------------------------------------------------------------------------------

// Cap first letter of every word Function
//
// function LetterCapitalize(str) {
//
//   var array = str.split(' ');
//
//   for (var i = 0; i < array.length; i++) {
//
//     array[i] = array[i].charAt(0).toUpperCase() + array[i].slice(1);
//
//   }
//
// return array.join(' ');
//
// }
//
// console.log(LetterCapitalize('adam is super cool.'));

//----------------------------------------------------------------------------------------------

// Change letters based on ASCII code position Function

// function letterChanges(str) {
// var newString = '';
// for (var i = 0; i < str.length; i++) {
//   newString += String.fromCharCode(str.charCodeAt(i) + 1);
// }
//   for (var j = 0; j < newString.length; j++) {
//     if (newString.charAt(j) === 'a' || newString.charAt(j) === 'e' || newString.charAt(j) === 'i' || newString.charAt(j) === 'o' || newString.charAt(j) === 'u') {
//      var capString = newString.replace(newString.charAt(j), newString.charAt(j).toUpperCase());
//   }
// }
//     return capString;
// }
//
// console.log(letterChanges("adam"));
// console.log(letterChanges('jen'));
// console.log(letterChanges('scott'));

//----------------------------------------------------------------------------------------------

//  Counter function

// var today = new Date();
// var start = new Date("March 21, 2016 09:00:00");
// var mathToday = today.getTime();
// var mathStart = start.getTime();
// var doMath = mathStart - mathToday;
// var converted = doMath / (1000 * 60 * 60 * 24);
// var rounded = Math.floor(converted);
//
// alert("School starts in " + rounded + " days!");

//-------------------------------------------------------------------------------------------

// Is Prime function

//Write a function that accepts a number and return a boolean based on whether it's a prime number.

// function prime(num) {
//   for(var i = 2; i < num, i++){
//     if(num % i === 0) {
//       return false;
//     }
//   }
//   return true;
// }
//
// console.log(isPrime(3));
// console.log(isPrime(10));

//-------------------------------------------------------------------------------------------------

// Missing number from an array of numbers

// function missingNo(array) {
//   var missingNum = [];
//   for(var i = 0; i < array.length; i++) {
//     if(array.indexOf(i) < 0) {
//       missingNum.push(i);
//     }
//   }
//   return missingNum;
// }
//
// console.log(missingNo([0, 1, 2, 3, 5]));

//----------------------------------------------------------------------------------------------
