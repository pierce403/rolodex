document.getElementById('rolodex-search-form').addEventListener('submit', function(e) {
    rolodexSearch();
    e.preventDefault();
}, false);

function rolodexSearch()
{      
  console.log("Running new search");
  
  // clear table before starting search
  let rolodexTable = document.getElementById("rolodex-table");
  rolodexTable.innerHTML = ""
       
  //search = document.getElementById("nweb-search").value;
  //document.getElementById("message").textContent = "Searching for '"+search+"'";

  rolodexResult = fetch('dump')
    .then(response => response.json())
    .then(function(data){
       let rolodexTable = document.getElementById("rolodex-table");
       console.log(data);
       rolodexTable.innerHTML = ""

  let fields = ['id','first_name','last_name']
  let row = rolodexTable.insertRow(-1);
  for(let field of fields)
  {
   row.insertCell().innerText = field;
  }

  console.log(data.keys());
  for(let person of data)
  {
   console.log(person);
   let row = rolodexTable.insertRow(-1);
   //left = host.ip+'\n\nhostname: '+host.hostname+'\nports: '+host.ports

   // add in all the desired fields
   for(let field of fields)
   {
    row.insertCell().innerText = person[field];
   }
  }
  //document.getElementById("message").textContent = "Searching for '"+search+"' *complete*";

  })
  

}

document.getElementById("rolodex-search").value="nmap";
//rolodexSearch();
