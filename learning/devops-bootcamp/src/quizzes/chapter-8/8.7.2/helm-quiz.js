const rawQuizdown = `
---
shuffleQuestions: true
shuffleAnswers: true
---
# True or False: It would be a good idea to create a reusable script to populate the values file for all Helm Charts that you use, in order to set up some basic commonalities between them.

1. [ ] True
    > Not quite. Since the configuration for each chart is left up to the producers of it, there is no guarantee that two charts will have the same values templates. It's always better to read the upstream values file for each chart that you use, to avoid accidental misconfiguration.
1. [x] False
    > Good. Since the configuration for each chart is left up to the producers of it, there is no guarantee that two charts will have the same values templates. It's always better to read the upstream values file for each chart that you use, to avoid accidental misconfiguration.

# What should you do if you need to make a change that the Helm Chart template doesn't support?

1. [x] Write a Kustomize patch to make the change.
    > Good. Kustomize patches can be used to make changes to the rendered Kubernetes manifests that Helm produces, without modifying the Helm Chart itself.
1. [ ] Send a support ticket to the chart maintainers.
    > This is a perfectly viable solution, so long as you're okay with waiting three years before your change works.
1. [ ] Fork the Helm Chart and make the change to the template directly.
    > This is not a good idea, as it would then require you to maintain this code, adding more scope to the project.
1. [ ] Make the change to the \`helm-chart.yaml\` file after inflating the chart.
    > This will only work temporarily, as the next time the chart is inflated your change will be lost.
1. [ ] Don't use the Helm Chart and pick a different one. There's nothing you can do.
    > Not with that attitude there isn't!

# Select all that apply: What can reading the upstream values file tell you about a Helm Chart?

- [x] The general schema that the chart expects.
- [x] The comprehensive list of keys that the chart accepts.
- [x] The default values that the chart uses.
- [ ] The comprehensive list of values that the chart accepts.
    > Not quite. While you can see all default values, you can't see all possible values that the chart accepts. This granularity does depend on the creators of the chart, but typically speaking they leave some obvious fields open-ended.

# True or False: All Helm Chart values are optional.

1. [x] True
    > Good. You don't even need a values file to source and inflate a Helm Chart, as all values have defaults.
1. [ ] False
    > Not quite. You don't even need a values file to source and inflate a Helm Chart, as all values have defaults.
`;

export { rawQuizdown }
