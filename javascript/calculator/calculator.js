/* ===========================
   Calculator – Logic
   =========================== */

(function () {
  "use strict";

  const display = document.getElementById("display");

  // State
  let currentInput = "";
  let previousInput = "";
  let operator = null;
  let shouldResetDisplay = false;

  // -------------------------------------------------------
  // Helpers
  // -------------------------------------------------------
  function updateDisplay(value) {
    display.textContent = value === "" ? "0" : value;
  }

  function calculate(a, op, b) {
    const numA = parseFloat(a);
    const numB = parseFloat(b);
    switch (op) {
      case "+": return numA + numB;
      case "-": return numA - numB;
      case "*": return numA * numB;
      case "/":
        if (numB === 0) return null;
        return numA / numB;
      default:  return numB;
    }
  }

  function formatResult(value) {
    // Limit floating-point noise (e.g. 0.1+0.2)
    const rounded = parseFloat(value.toPrecision(10));
    return String(rounded);
  }

  // -------------------------------------------------------
  // Actions
  // -------------------------------------------------------
  function inputDigit(digit) {
    if (shouldResetDisplay) {
      currentInput = digit;
      shouldResetDisplay = false;
    } else {
      currentInput = currentInput === "0" ? digit : currentInput + digit;
    }
    updateDisplay(currentInput);
  }

  function inputDecimal() {
    if (shouldResetDisplay) {
      currentInput = "0.";
      shouldResetDisplay = false;
      updateDisplay(currentInput);
      return;
    }
    if (!currentInput.includes(".")) {
      currentInput = (currentInput || "0") + ".";
      updateDisplay(currentInput);
    }
  }

  function handleOperator(op) {
    if (operator && !shouldResetDisplay) {
      // Chain: evaluate the pending operation first
      const result = calculate(previousInput, operator, currentInput);
      if (result === null) {
        updateDisplay("Error");
        currentInput = "";
        previousInput = "";
        operator = null;
        shouldResetDisplay = true;
        return;
      }
      currentInput = formatResult(result);
      updateDisplay(currentInput);
    }
    previousInput = currentInput;
    operator = op;
    shouldResetDisplay = true;
  }

  function handleEquals() {
    if (!operator || shouldResetDisplay) return;
    const result = calculate(previousInput, operator, currentInput);
    if (result === null) {
      updateDisplay("Error");
      currentInput = "";
    } else {
      currentInput = formatResult(result);
      updateDisplay(currentInput);
    }
    previousInput = "";
    operator = null;
    shouldResetDisplay = true;
  }

  function handleClear() {
    currentInput = "";
    previousInput = "";
    operator = null;
    shouldResetDisplay = false;
    updateDisplay("0");
  }

  function handleBackspace() {
    if (shouldResetDisplay) return;
    currentInput = currentInput.slice(0, -1);
    updateDisplay(currentInput || "0");
  }

  // -------------------------------------------------------
  // Button click handler (event delegation)
  // -------------------------------------------------------
  document.querySelector(".buttons").addEventListener("click", function (e) {
    const btn = e.target.closest(".btn");
    if (!btn) return;

    const action = btn.dataset.action;
    const value  = btn.dataset.value;

    switch (action) {
      case "digit":     inputDigit(value);    break;
      case "decimal":   inputDecimal();       break;
      case "operator":  handleOperator(value);break;
      case "equals":    handleEquals();       break;
      case "clear":     handleClear();        break;
      case "backspace": handleBackspace();    break;
    }
  });

  // -------------------------------------------------------
  // Keyboard support
  // -------------------------------------------------------
  document.addEventListener("keydown", function (e) {
    if (e.key >= "0" && e.key <= "9")          inputDigit(e.key);
    else if (e.key === ".")                     inputDecimal();
    else if (["+", "-", "*", "/"].includes(e.key)) handleOperator(e.key);
    else if (e.key === "Enter" || e.key === "=") handleEquals();
    else if (e.key === "Backspace")             handleBackspace();
    else if (e.key === "Escape" || e.key === "c" || e.key === "C") handleClear();
  });
})();
