import Search from "./Search"
import styles from "./Header.module.css"

const Header = (props: { count: number | undefined }) => (
	<header class={styles.header}>
		<Search count={props.count} />
	</header>
)

export default Header
