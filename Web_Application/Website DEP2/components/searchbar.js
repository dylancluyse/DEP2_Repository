import React, { useState } from 'react';

function SearchBar() {
  const [searchValue, setSearchValue] = useState('');

  const handleChange = (event) => {
    setSearchValue(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    //
  };

  return (
    <form class='flex items-center justify-start w-96 ml-5 pb-5'>
      <input
        class='flex-grow px-2 py-1 rounded-lg mr-2 w-16'
        type='text'
        placeholder='Search...'
        value={searchValue}
        onChange={handleChange}
      ></input>
      <button
        class='px-2 py-1 rounded-lg bg-blue-500 text-white'
        type='submit'
        on
      >
        Search
      </button>
    </form>
  );
}
export default SearchBar;
