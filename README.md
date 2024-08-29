import { Box, Button, TextField, Typography, Grid } from '@mui/material';
import { useState } from 'react';

const ContractForm = () => {
  const [contractNumber, setContractNumber] = useState('');
  const [firstPaymentDue, setFirstPaymentDue] = useState('');
  const [discountDate, setDiscountDate] = useState('');
  const [totalFinancedValue, setTotalFinancedValue] = useState('');
  const [liquidReleasedValue, setLiquidReleasedValue] = useState('');
  const [creditReleaseDate, setCreditReleaseDate] = useState('');
  const [installmentQuantity, setInstallmentQuantity] = useState('');
  const [monthlyInterest, setMonthlyInterest] = useState('');
  const [cet, setCet] = useState('');
  const [iofValue, setIofValue] = useState('');
  const [graceDays, setGraceDays] = useState('');
  const [carenciaValue, setCarenciaValue] = useState('');
  const [observations, setObservations] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Lógica para manipular o envio do formulário
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Typography variant="h6">Informações do Contrato</Typography>
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Número do Contrato"
            fullWidth
            value={contractNumber}
            onChange={(e) => setContractNumber(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Vencimento 1ª Parcela"
            type="date"
            fullWidth
            InputLabelProps={{
              shrink: true,
            }}
            value={firstPaymentDue}
            onChange={(e) => setFirstPaymentDue(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Folha 1º Desconto"
            fullWidth
            value={discountDate}
            onChange={(e) => setDiscountDate(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Valor Total Financiado"
            fullWidth
            value={totalFinancedValue}
            onChange={(e) => setTotalFinancedValue(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Valor Líquido Liberado"
            fullWidth
            value={liquidReleasedValue}
            onChange={(e) => setLiquidReleasedValue(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Data de Liberação do Crédito"
            type="date"
            fullWidth
            InputLabelProps={{
              shrink: true,
            }}
            value={creditReleaseDate}
            onChange={(e) => setCreditReleaseDate(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Quantidade de Parcelas"
            fullWidth
            value={installmentQuantity}
            onChange={(e) => setInstallmentQuantity(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Juros Mensal"
            fullWidth
            value={monthlyInterest}
            onChange={(e) => setMonthlyInterest(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="CET"
            fullWidth
            value={cet}
            onChange={(e) => setCet(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Valor IOF"
            fullWidth
            value={iofValue}
            onChange={(e) => setIofValue(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Dias de Carência"
            fullWidth
            value={graceDays}
            onChange={(e) => setGraceDays(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Valor Carência"
            fullWidth
            value={carenciaValue}
            onChange={(e) => setCarenciaValue(e.target.value)}
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            label="Observações"
            fullWidth
            multiline
            rows={4}
            value={observations}
            onChange={(e) => setObservations(e.target.value)}
          />
        </Grid>
        <Grid item xs={12}>
          <Button variant="outlined" color="error">
            Cancelar
          </Button>
          <Button type="submit" variant="contained" sx={{ ml: 2 }}>
            Próximo
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ContractForm;
