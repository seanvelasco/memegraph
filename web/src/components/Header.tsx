import styles from "./Header.module.css"
import type { JSXElement } from "solid-js"

const Header = (props: { children: JSXElement }) => (
	<header class={styles.header}>{props.children}</header>
)

export default Header
