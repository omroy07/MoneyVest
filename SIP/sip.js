document.getElementById('calculateBtn').addEventListener('click', function () {
  const P = parseFloat(document.getElementById('monthlyInvestment').value);
  const r = parseFloat(document.getElementById('annualReturn').value) / 100 / 12; // monthly rate
  const n = parseFloat(document.getElementById('investmentDuration').value) * 12; // total months

  const resultDiv = document.getElementById('result');

  if (isNaN(P) || P <= 0) {
    alert('Please enter a valid monthly investment amount.');
    return;
  }
  if (isNaN(r) || r < 0) {
    alert('Please enter a valid expected annual return rate.');
    return;
  }
  if (isNaN(n) || n <= 0) {
    alert('Please enter a valid investment duration.');
    return;
  }

  // SIP Future Value formula: FV = P * [ ( (1 + r)^n - 1 ) / r ] * (1 + r)
  const fv = P * (((Math.pow(1 + r, n) - 1) / r) * (1 + r));
  const totalInvested = P * n;

  resultDiv.style.display = 'block';
  resultDiv.innerHTML = `
    <p>Total Invested Amount: ₹${totalInvested.toFixed(2)}</p>
    <p><strong>Estimated Maturity Amount: ₹${fv.toFixed(2)}</strong></p>
  `;
});
