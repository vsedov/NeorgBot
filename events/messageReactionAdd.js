const { MessageEmbed } = require('discord.js')

module.exports = {
	name: 'messageReactionAdd',
	once: false,

	async execute(payload, user) {
		const content = await payload.message.content
		const emoji = await payload.emoji.name
		const author = await payload.message.author

		if (content) {
			if ("🔖📑".includes(emoji)) {
				const em = new MessageEmbed()
					.setDescription(`
				**From: <@${author.id}> **
				${content}
				`)
					.setColor("RED")
				await user.send({ embeds: [em] })
			}
		}
	},
};
