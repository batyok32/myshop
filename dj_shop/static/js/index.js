// Get Input Fields
const name = document.getElementById("name");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirmPassword");
const email = document.getElementById("email");

// Get Form
const form = document.getElementById("form");

// Validators
function validateName() {
  // check if empty
  if (checkIfEmpty(name)) return;
  // check if it contains only letter
  if (!checkIfOnlyLetters(name)) return;
  return true;
}

function validatePassword() {
  if (checkIfEmpty(password)) return;
  //   must be of certain length
  if (!meetLength(password, 6, 100)) return;
  // check length against our character set
  //   1. a
  if (!contiansCharaters(password, 2)) {
  }
  //   2. a - 1
  //   3. A-a-1
  //   4. A-a-1-symbol
  return true;
}

function validateConfirmPassword() {
  if (password.className != "valid") {
    setInvalid(confirmPassword, "Password must be valid");
    return;
  }
  //   check if they match
  if (password.value !== confirmPassword.value) {
    setInvalid(confirmPassword, "Password must match");
  } else {
    setValid(confirmPassword);
  }
  return true;
}

// Utilities
function checkIfEmpty(field) {
  if (isEmpty(field.value.trim())) {
    // set Invalid
    setInvalid(field, "required");
    return true;
  } else {
    //   set Valid
    setValid(field);
  }
}

function isEmpty(value) {
  if (value === "") return true;
  return false;
}

function setInvalid(field, message) {
  field.className = "invalid";
  field.nextElementSibling.innerHTML = message;
  field.nextElementSibling.style.color = "#f23452";
}

function setValid(field) {
  field.className = "valid";
  field.className = "valid";
  field.nextElementSibling.innerHTML = "";
}

function checkIfOnlyLetters(field) {
  if (/^[a-zA-Z ]+$/.test(field.value)) {
    setValid(field);
    return true;
  } else {
    setInvalid(field, "must contain only letters");
    return false;
  }
}

function meetLength(field, minLength, maxLength) {
  if (field.value.length >= minLength && field.value.length < maxLength) {
    setValid(field);
    return true;
  } else if (field.value.length < minLength) {
    setInvalid(field, `must be at least ${minLength} characters`);
    return false;
  } else if (field.value.length >= maxLength) {
    setInvalid(field, `must be less than ${maxLength} characters`);
    return false;
  }
}

function contiansCharaters(field, code) {
  let regex;
  switch (code) {
    case 1:
      // At least a letter
      regex = /(?=.*[a-zA-Z])/;
      return matchRegularExp(regex, field, "Must contain at least a letter");
    case 2:
      // At least a letter and  a number
      regex = /^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)[0-9a-zA-Z]{6,}$/;
      return matchRegularExp(
        regex,
        field,
        "Must contain at least a letter and a number"
      );
    default:
      return false;
  }
}

function matchRegularExp(regex, field, message) {
  if (field.value.match(regex)) {
    setValid(field);
    return true;
  } else {
    setInvalid(field, message);
    return false;
  }
}
