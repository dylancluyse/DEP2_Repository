import {
  Box,
  FormControl,
  FormHelperText,
  Input,
  InputLabel,
  MenuItem,
  Select,
} from '@mui/material';
import { useEffect, useState } from 'react';
import useSWR from 'swr';
import fetcher from '../lib/fetcher';

export default function AdminPredictions(props) {
  const { urb, bal, omz, pers, age } = props;

  const { data: pred, error } = useSWR(
    `http://localhost:8000/admin/predict?urbanisation=${urb}&balance_total=${bal}&revenue=${omz}&employees=${pers}&years=${age}`,
    fetcher
  );
  if (error) return <div>failed to load</div>;
  if (!pred) return <div>loading...</div>;

  const {env, soc, gov, max, linregcalc, rfr, lr_score} = pred.data;
  console.log(pred)

  return (
    <div className='snap-center p-5'>
      <h1 className='font-bold'>Neurale netwerk</h1>
      <p>Het neurale netwerk model voorspelt de volgende percentielen per domein.</p>
      <ul>
          <li>Environment: { env } </li>
          <li>Social: { soc } </li>
          <li>Governance: { gov } </li>
      </ul>
      
      <h1 className='font-bold pt-3'>Lineaire Regressie</h1>
      <p>Dit model voorspelt dat de algemene score van dit bedrijf in het { lr_score }e percentiel zal liggen.</p> 
      <p>Deze voorspelling gebeurt op basis van de volgende berekening: </p>
      <p>{ linregcalc } </p>

      <h1 className='font-bold pt-3'>Random Forest Regressie</h1>
      <p>Dit model voorspelt dat de algemene score van dit bedrijf in het { rfr }e percentiel zal liggen.</p>
    </div>
  );
}
