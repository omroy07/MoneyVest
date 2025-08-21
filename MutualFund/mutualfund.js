document.getElementById('mfCalculateBtn').addEventListener('click', function () {
  const initial = parseFloat(document.getElementById('initialInvestment').value);
  const annualCont = parseFloat(document.getElementById('annualContribution').value);
  const rate = parseFloat(document.getElementById('mfAnnualReturn').value) / 100;
  const years = parseFloat(document.getElementById('mfDuration').value);

  const resultDiv = document.getElementById('mfResult');

  if (isNaN(initial) || initial <= 0) {
    alert('Please enter a valid initial investment amount.');
    return;
  }
  if (isNaN(annualCont) || annualCont < 0) {
    alert('Please enter a valid annual contribution (0 or more).');
    return;
  }
  if (isNaN(rate) || rate < 0) {
    alert('Please enter a valid expected annual return rate.');
    return;
  }
  if (isNaN(years) || years <= 0) {
    alert('Please enter a valid investment duration.');
    return;
  }

  // Calculate future value:
  // FV = initial * (1 + r)^n + annualContribution * [ ((1 + r)^n - 1) / r ]
  const fvInitial = initial * Math.pow(1 + rate, years);
  let fvAnnual = 0;
  if (rate === 0) {
    fvAnnual = annualCont * years;
  } else {
    fvAnnual = annualCont * ( (Math.pow(1 + rate, years) - 1) / rate );
  }
  const totalFV = fvInitial + fvAnnual;
  const totalInvested = initial + annualCont * years;

  resultDiv.style.display = 'block';
  resultDiv.innerHTML = `
    <p>Total Invested Amount: ₹${totalInvested.toFixed(2)}</p>
    <p><strong>Estimated Maturity Amount: ₹${totalFV.toFixed(2)}</strong></p>
  `;
});
