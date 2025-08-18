const silverForm = document.getElementById('silverForm');
const silverList = document.getElementById('silverList');
const silverTotalValueElem = document.getElementById('silverTotalValue');

let silverHoldings = [];

silverForm.addEventListener('submit', function (e) {
  e.preventDefault();

  const weight = parseFloat(document.getElementById('silverWeight').value);
  const price = parseFloat(document.getElementById('silverPrice').value);

  if (isNaN(weight) || weight <= 0 || isNaN(price) || price < 0) {
    alert('Please enter valid weight and price.');
    return;
  }

  silverHoldings.push({ weight, price });

  updateSilverHoldings();

  silverForm.reset();
});

function updateSilverHoldings() {
  silverList.innerHTML = '';

  if (silverHoldings.length === 0) {
    silverList.innerHTML = '<li>No silver holdings added yet.</li>';
    silverTotalValueElem.textContent = '0.00';
    return;
  }

  let totalValue = 0;

  silverHoldings.forEach(({ weight, price }) => {
    const value = weight * price;
    totalValue += value;

    const li = document.createElement('li');
    li.textContent = `${weight.toFixed(2)} grams @ ₹${price.toFixed(2)} = ₹${value.toFixed(2)}`;
    silverList.appendChild(li);
  });

  silverTotalValueElem.textContent = totalValue.toFixed(2);
}
