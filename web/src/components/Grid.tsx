import { For, useTransition } from "solid-js"
import { A } from "@solidjs/router"
import Image from "./Image"
import styles from "./Grid.module.css"

const Grid = (props: { images: { id: string }[] }) => {
	const [pending] = useTransition()

	return (
		<div classList={{ pending: pending() }} class={styles.grid}>
			<For each={props.images}>
				{(image) => (
					<A href={"/" + image.id}>
						<Image {...image} />
					</A>
				)}
			</For>
		</div>
	)
}

export default Grid
