import styles from "./Fallback.module.css"

const Fallback = () => {
	return (
		<div class={styles.fallback}>
			<img class={styles.image} src="/404.gif" />
		</div>
	)
}

export default Fallback
