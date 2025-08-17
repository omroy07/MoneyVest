const goldForm = document.getElementById('goldForm');
const goldList = document.getElementById('goldList');
const totalValueElem = document.getElementById('totalValue');

let holdings = [];

goldForm.addEventListener('submit', function (e) {
  e.preventDefault();

  const weight = parseFloat(document.getElementById('goldWeight').value);
  const price = parseFloat(document.getElementById('goldPrice').value);

  if (isNaN(weight) || weight <= 0 || isNaN(price) || price < 0) {
    alert('Please enter valid weight and price.');
    return;
  }

  holdings.push({ weight, price });

  updateHoldings();

  goldForm.reset();
});

function updateHoldings() {
  goldList.innerHTML = '';

  if (holdings.length === 0) {
    goldList.innerHTML = '<li>No gold holdings added yet.</li>';
    totalValueElem.textContent = '0.00';
    return;
  }

  let totalValue = 0;

  holdings.forEach(({ weight, price }) => {
    const value = weight * price;
    totalValue += value;

    const li = document.createElement('li');
    li.textContent = `${weight.toFixed(2)} grams @ ₹${price.toFixed(2)} = ₹${value.toFixed(2)}`;
    goldList.appendChild(li);
  });

  totalValueElem.textContent = totalValue.toFixed(2);
}
