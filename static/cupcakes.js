const BASE_URL = "http://localhost:5000/api"

function cupcakeHtml(cupcake) {
  return `
    <div data-cupcake-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-button">🚮</button>
      </li>
      <img class="cupcake-img"
            src="${cupcake.image}"
            alt="cupcake">
    </div>
  `
}


async function showCupcakes() {
  const resp = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcakeData of resp.data.cupcakes) {
    let cupcake = $(cupcakeHtml(cupcakeData))
    $("#cupcakes-list").append(cupcake)
  }
}


$("#new-cupcake-form").on("submit", async function (e) {
  e.preventDefault();
  let flavor = $("#form-flavor").val()
  let rating = $("#form-rating").val()
  let size = $("#form-size").val()
  let image = $("#form-image").val()

  const newCupcakeResp = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image
  })

  let newCupcake = $(cupcakeHtml(newCupcakeResp.data.cupcake))
  $("#cupcakes-list").append(newCupcake)
})


$("#cupcakes-list").on("click", ".delete-button", async function (e) {
  e.preventDefault();
  let $cupcake = $(e.target).closest("div")
  let cupcakeId = $cupcake.attr("data-cupcake-id")
  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`)
  $cupcake.remove()
})


$(showCupcakes)