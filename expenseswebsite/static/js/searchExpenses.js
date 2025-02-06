document.getElementById("filterBtn").addEventListener("click", function () {
  const startDate = document.getElementById("startDate").value;
  const endDate = document.getElementById("endDate").value;
  const category = document.getElementById("category").value;
  const customer = document.getElementById("customer").value;
  const searchQuery = document.getElementById("searchField").value;

  // Construct the URL with query parameters
  let url = new URL(window.location.href);

  // Append filter parameters to the URL
  if (startDate) url.searchParams.set("start_date", startDate);
  if (endDate) url.searchParams.set("end_date", endDate);
  if (category) url.searchParams.set("category", category);
  if (customer) url.searchParams.set("customer", customer);
  if (searchQuery) url.searchParams.set("search", searchQuery);

  // Reload the page with the updated filters
  window.location.href = url.toString();
});
