const stocksForm = document.getElementById('stocksForm');
const stocksList = document.getElementById('stocksList');
const stocksTotalValueElem = document.getElementById('stocksTotalValue');

let stockHoldings = [];

stocksForm.addEventListener('submit', function (e) {
  e.preventDefault();

  const name = document.getElementById('stockName').value.trim();
  const shares = parseInt(document.getElementById('stockShares').value);
  const price = parseFloat(document.getElementById('stockPrice').value);

  if (!name || isNaN(shares) || shares <= 0 || isNaN(price) || price < 0) {
    alert('Please enter valid stock name, shares, and price.');
    return;
  }

  stockHoldings.push({ name, shares, price });

  updateStockHoldings();

  stocksForm.reset();
});

function updateStockHoldings() {
  stocksList.innerHTML = '';

  if (stockHoldings.length === 0) {
    stocksList.innerHTML = '<li>No stock holdings added yet.</li>';
    stocksTotalValueElem.textContent = '0.00';
    return;
  }

  let totalValue = 0;

  stockHoldings.forEach(({ name, shares, price }) => {
    const value = shares * price;
    totalValue += value;

    const li = document.createElement('li');
    li.textContent = `${name.toUpperCase()} — ${shares} shares @ ₹${price.toFixed(2)} = ₹${value.toFixed(2)}`;
    stocksList.appendChild(li);
  });

  stocksTotalValueElem.textContent = totalValue.toFixed(2);
}
