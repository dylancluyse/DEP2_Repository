import * as React from 'react';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import makeStyles from '@mui/material/styles/makeStyles';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import useSWR, { mutate } from 'swr';
import fetcher from '../lib/fetcher';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { formatGraphDataToPercentages } from '../utils/graphFormatter.js';


function matchScoreToWords(words, score) {
  const out = []
  words.forEach((element, index) => {
    out.push({
      name: element,
      score: score[index]
    }) 
  });
  console.log(out)
  return out;
  // return [Object.assign(...words.map((k, i) => ({[k]: score[i]})))]

}

const CompanyScoresView = ({
  subdomein,
  scoreSubdomeinEnvironment,
  subdomainInformation,
}) => {
  // const data = [
  //   {
  //     name: 'Environment',
  //     score: scoreSubdomeinEnvironment[0],
  //   },
  //   {
  //     name: 'Social',
  //     score: scoreSubdomeinEnvironment[1],
  //   },
  //   {
  //     name: 'Governance',
  //     score: scoreSubdomeinEnvironment[2],
  //   },
  // ];
  const data = formatGraphDataToPercentages(matchScoreToWords(subdomainInformation, scoreSubdomeinEnvironment), ["score"]) 
  // const data = matchScoreToWords(subdomainInformation, scoreSubdomeinEnvironment) 

const colors = [ '#8884d8', '#82ca9d', '#ff7f0e', '#2ca02c', '#d62728', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5',
];
  console.log(data)

  return (
    <Card class=' p-5 bg-gradient-to-r from-light-yellow to-light-yellow'>
      <CardContent class='grid justify-center grid-cols-1 gap-0.5 '>
        <Typography variant='p' component='p'>
          Scores voor subdomein {subdomein}:
        </Typography>

        <BarChart
          width={380}
          height={280}
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray='3 3' />
          <XAxis dataKey='name' interval={-1} />
          <YAxis domain={[0, 100]}/>
          <Tooltip />
          <Legend />
          <Bar dataKey='score' fill='#8884d8' label={false} name={`Score ${subdomein}`}/>
        </BarChart>

      </CardContent>
    </Card>
  );
};

export const CompanySubDomainScoresOverviewEnvironment = (props) => {
  if (!props.company) {
    return "";
  }

  const { data: companyList, error } = useSWR(
    `http://localhost:8000/company/${props.company}`,
    fetcher
  );
  if (error) return <div>failed to load</div>;
  if (!companyList) return <div>loading...</div>;

  const { data: company } = companyList;

  return (
    <Box
      sx={{
        width: '100%',
        bgcolor: 'background.paper',
      }}
    >
      <div>
        <CompanyScoresView
          subdomein="Environment"
          scoreSubdomeinEnvironment={company.subdomeinen_environment}
          subdomainInformation={props.subdomainInformation["Environment"]}
        />
      </div>
    </Box>
  );
};


export const CompanySubDomainScoresOverviewSocial = (props) => {
  if (!props.company) {
    return "";
  }

  const { data: companyList, error } = useSWR(
    `http://localhost:8000/company/${props.company}`,
    fetcher
  );
  if (error) return <div>failed to load</div>;
  if (!companyList) return <div>loading...</div>;

  const { data: company } = companyList;

  return (
    <Box
      sx={{
        width: '100%',
        bgcolor: 'background.paper',
      }}
    >
      <div>
        <CompanyScoresView
          subdomein="Social"
          scoreSubdomeinEnvironment={company.subdomeinen_social}
          subdomainInformation={props.subdomainInformation["Social"]}
        />
      </div>
    </Box>
  );
};

export const CompanySubDomainScoresOverviewGovernance = (props) => {
  if (!props.company) {
    return "";
  }

  const { data: companyList, error } = useSWR(
    `http://localhost:8000/company/${props.company}`,
    fetcher
  );
  if (error) return <div>failed to load</div>;
  if (!companyList) return <div>loading...</div>;

  const { data: company } = companyList;

  return (
    <Box
      sx={{
        width: '100%',
        bgcolor: 'background.paper',
      }}
    >
      <div>
        <CompanyScoresView
          subdomein="Governance"
          scoreSubdomeinEnvironment={company.subdomeinen_governance}
          subdomainInformation={props.subdomainInformation["Governance"]}
        />
      </div>
    </Box>
  );
};
