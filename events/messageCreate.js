module.exports = {
	name: 'messageCreate',
	once: false,

	execute(mess) {
		if (mess.content.includes("sus")) mess.react("<:sus:867395030988881921>");
	},
};
