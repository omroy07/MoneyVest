const expenseForm = document.getElementById('expenseForm');
const expenseList = document.getElementById('expenseList');

let expenses = [];

expenseForm.addEventListener('submit', function (e) {
  e.preventDefault();

  const name = document.getElementById('expenseName').value.trim();
  const amount = parseFloat(document.getElementById('expenseAmount').value);
  const date = document.getElementById('expenseDate').value;

  if (!name || isNaN(amount) || amount <= 0 || !date) {
    alert('Please enter valid expense details.');
    return;
  }

  const expense = { name, amount, date };
  expenses.push(expense);

  displayExpenses();

  // Reset form
  expenseForm.reset();
});

function displayExpenses() {
  expenseList.innerHTML = '';

  if (expenses.length === 0) {
    expenseList.innerHTML = '<li>No expenses added yet.</li>';
    return;
  }

  expenses.forEach(({ name, amount, date }, index) => {
    const li = document.createElement('li');

    li.innerHTML = `
      <span>${name} (${date})</span>
      <span class="amount">₹${amount.toFixed(2)}</span>
    `;

    expenseList.appendChild(li);
  });
}
