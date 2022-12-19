
function toPercentage(number) {
  return parseFloat((number * 100).toFixed(2))
}

export const formatGraphDataToPercentages = (data, keys) => {

  return data.map(item => {
    const formattedItem = { ...item }
    keys.forEach(key => {
      formattedItem[key] = toPercentage(item[key])
    });
    return formattedItem;
  });
};

