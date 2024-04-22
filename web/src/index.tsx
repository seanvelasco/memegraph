/* @refresh reload */
import { render } from "solid-js/web"
import { MetaProvider } from "@solidjs/meta"
import { Router, Route } from "@solidjs/router"

import App from "./App"
import { HomePage, ImagePage } from "./App"

const root = document.getElementById("root")

render(
	() => (
		<MetaProvider>
			<Router root={App}>
				<Route path="/" component={HomePage} />
				<Route path="/:image" component={ImagePage} />
			</Router>
		</MetaProvider>
	),
	root!
)
