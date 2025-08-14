const categories = ['Salary', 'Mutual Funds', 'SIPs', 'Stocks', 'Gold', 'Silver', 'Fixed Deposits', 'Expense'];
const defaultData = Array(categories.length).fill(0);
let chart;

window.onload = () => {
  const formGrid = document.getElementById('formGrid');
  const cardsGrid = document.getElementById('cardsGrid');

  // Create input fields
  categories.forEach((cat, i) => {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
      <label for="input-${i}">${cat}</label>
      <input type="number" id="input-${i}" min="0" value="0" step="any"/>
    `;
    formGrid.appendChild(wrapper);
  });

  // Create summary cards
  categories.forEach((cat, i) => {
    const card = document.createElement('div');
    card.className = 'card';
    card.id = `card-${i}`;
    card.innerText = `${cat}: ₹0`;
    cardsGrid.appendChild(card);
  });

  // Create chart
  const ctx = document.getElementById('portfolioChart').getContext('2d');
  chart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: categories,
      datasets: [{
        data: defaultData,
        backgroundColor: [
          '#00668E', '#17BECF', '#38A86F', '#FFC20A',
          '#E07466', '#9B59B6', '#E67E22', '#C9495E'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' },
        title: { display: true, text: 'Portfolio Distribution (₹)' }
      }
    }
  });

  // Add input listener to update data
  formGrid.addEventListener('input', () => {
    const values = categories.map((_, i) => {
      const val = parseFloat(document.getElementById(`input-${i}`).value);
      return isNaN(val) ? 0 : val;
    });

    // Update cards
    values.forEach((val, i) => {
      document.getElementById(`card-${i}`).innerText = `${categories[i]}: ₹${val.toLocaleString('en-IN')}`;
    });

    // Update chart
    chart.data.datasets[0].data = values;
    chart.update();
  });
};
