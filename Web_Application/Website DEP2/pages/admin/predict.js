import { Link, Button, Slider } from '@mui/material';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import useSWR from 'swr';
import AdminPredictions from '../../components/admin-prediction.js';
import fetcher from '../../lib/fetcher';

const Predict = () => {
  
  const [urb, setUrb] = useState(1)
  const [bal, setBal] = useState(0)
  const [omz, setOmz] = useState(0)
  const [pers, setPers] = useState(0)
  const [age, setAge] = useState(0)
  const [prediction, setPrediction] = useState("fo")
  const [isSet, setIsSet] = useState(false)


  const handleSlider = (e, numb) => {
    setUrb(numb)
    console.log(urb)
  }

  const doSomething = (event) => {
    event.preventDefault();
    console.log(event.target)
    console.log(urb)
    console.log(bal)
    console.log(omz)
    console.log(pers)
    console.log(age)
    setPrediction('reee')
    setIsSet(true)


    // const { domains: doms, categories } = keywords;

    // const foo = createKeywordList(doms);
  }


  return (
    <div className=' min-h-screen py-2  max-h-screen bg-Grijs'>
      <a
        href='/'
        class=' absolute mt-2 mb-5 m-5 text-white bg-lichtblauw font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2  z-10'
      >
        Home
      </a>
      <main className='mt-28 flex flex-col items-center justify-center w-full flex-1 sm:px-20 my-10 '>
        <h1 className='text-4xl sm:text-6xl font-bold'>
          Admin - Predict Score
        </h1>

        <form className='grid' onSubmit={doSomething}>
            <label for="param1">Geef de verstedelijkingsgraad in:</label>
            <Slider
              aria-label="Small steps"
              step={0.01}
              min={0.00}
              max={2.00}
              value={urb}
              valueLabelDisplay="auto"
              onChange={handleSlider}
            />

            <label for="param2">Geef de balanstotaal in:</label>
            <input type="number" name="param2" id="param1" onChange={(event) => {setBal(event.target.value)}}/>

            <label for="param3">Geef de omzet in:</label>
            <input type="number" name="param3" id="param2" onChange={(event) => {setOmz(event.target.value)}}/>

            <label for="param4">Geef de personeelsbestanden in:</label>
            <input type="number" name="param4" id="param3" onChange={(event) => {setPers(event.target.value)}}/>

            <label for="param5">Geef de leeftijd van het bedrijf in jaren in:</label>
            <input type="number" name="param5" id="param4" onChange={(event) => {setAge(event.target.value)}}/>

            <button type="submit">Submit</button>

        </form>
        <div className='py-20'>
        {isSet && <AdminPredictions urb={urb} bal={bal} omz={omz} pers={pers} age={age}/>}
        </div>
        
      </main>
    </div>
  );
};

export default Predict;
