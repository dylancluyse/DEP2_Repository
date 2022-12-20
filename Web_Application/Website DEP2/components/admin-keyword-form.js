import useSWR from 'swr';
import fetcher from '../../lib/fetcher';


export default function keywords() {

  const { data: keywords, error } = useSWR(
    `http://localhost:8000/admin/keywords`,
    fetcher
  );
  if (error) return <div>failed to load</div>;
  if (!keywords) return <div>loading...</div>;

  const foo = createKeywordList(keywords)

  return (
    <div>
      <h1> Keywords </h1>
      <div className="flex">
        <p> foo </p>    
      </div>
      <div className="flex">
        {foo}    
      </div>
    </div>
  )
}

