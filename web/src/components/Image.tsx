import { Show, createSignal } from "solid-js"
import { BASE_BUCKET_URL } from "../lib/constant"
import styles from "./Image.module.css"

type ImageProps = {
	id: string
	distance?: number
	similarity?: number
	page?: boolean
}

const Image = (props: ImageProps) => {
	const [loaded, setLoaded] = createSignal(false)

	return (
		<div class={styles.wrapper}>
			<Show when={props.distance && loaded()}>
				<div class={styles.stat}>
					<span>{props.distance}</span>
					<span>{props.similarity}%</span>
				</div>
			</Show>
			<img
				class={props.page ? styles.page : styles.img}
				src={`${BASE_BUCKET_URL}/${props.id}`}
				onload={() => setLoaded(true)}
				loading="eager"
			/>
		</div>
	)
}

export default Image
