function get_scenes()
{
	fetch("/get_scenes")
	.then((response) => response.json())
	.then((json) => {
		console.log(json)
		const scene_control_div = document.getElementById("scene-controls")

		for (let i = 0; i < json.length; i++) {
			const button = document.createElement("button")
			const scene_name = json[i]["name"]
			button.innerHTML = scene_name 
			button.addEventListener('click', () => {
				fetch(`/switch_scene?scene_name=${scene_name}`)
			})
			scene_control_div.appendChild(button)
		}
	})
}

get_scenes()