
// Returns true if 2 arrays are equal and false otherwise
function arraysEqual(arr1, arr2) {

  if (arr1.length != arr2.length) return false;

  for (i = 0; i < arr1.length; i++) {
    if (arr1[i] != arr2[i]) return false;
  }

  return true;
}

// Returns if 2 objects are the same
// REQUIRES: arguments are key -> array
function objectsEqual(obj1,obj2) {
  var o1_keys = Object.keys(obj1);
  var o2_keys = Object.keys(obj2);

  // check if the keys are equal
  if (arraysEqual(o1_keys, o2_keys) == false) return false;

  // Now, check if all the component elements are the same.
  for (i = 0; i < o1_keys.length; i++) {
    if (arraysEqual(obj1[o1_keys[i]], obj2[o2_keys[i]]) == false) return false; 
  }

  return true;
}