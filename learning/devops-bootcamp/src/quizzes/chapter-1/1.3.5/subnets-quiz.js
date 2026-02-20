const rawQuizdown = `
---
shuffleAnswers: true
---

# Select all that will fall in the network address \`110.5.50.27/8\`

- [x] 110.10.15.20
- [x] 110.0.100.50
- [x] 110.5.50.25
- [ ] 132.20.15.100
- [ ] 55.28.13.155

# Select all that will fall in the network address \`110.5.50.27/16\`

- [x] 110.5.15.20
- [x] 110.5.100.50
- [x] 110.5.50.25
- [ ] 110.20.15.100
- [ ] 55.28.13.155

# Select all that will fall in the network address \`110.5.50.27/24\`

- [x] 110.5.50.20
- [x] 110.5.50.25
- [ ] 110.5.100.50
- [ ] 110.20.50.100
- [ ] 55.5.50.100

# Identify which of the following IP addresses fall within the reserved private IP address ranges. Select all that apply.

- [x] \`10.255.255.255/8\` 
  > \`10.255.255.255/8\` is within the \`10.0.0.0 - 10.255.255.255\` range, a private network range.
- [x] \`192.168.100.100/16\` 
  > \`192.168.100.100/16\` falls within the \`192.168.0.0 - 192.168.255.255\` range, which is reserved for private networks.
- [ ] \`172.15.0.1/12\` 
  > \`172.15.0.1/12\` is just outside the \`172.16.0.0 - 172.31.255.255\` private range.
- [ ] \`192.167.255.255/16\` 
  > \`192.167.255.255/16\` is close to but not within the \`192.168.0.0 - 192.168.255.255\` private range.
- [ ] \`11.0.0.0/8\`
  > \`11.0.0.0/8\` is outside the private range, as private IPs in this block start at \`10.0.0.0/8\`.
- [ ] \`172.32.0.0/12\` 
  > 172.32.0.0/12\` is just outside the upper boundary of the \`172.16.0.0 - 172.31.255.255\` private range.
- [ ] \`169.254.1.1/16\` 
  > \`169.254.1.1/16\` is a link-local address, used for auto-configuration when no IP is assigned by DHCP. It's not classified under traditional private ranges, but it's not routable on the public internet.
`;

export { rawQuizdown }