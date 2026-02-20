const rawQuizdown = `
---
shuffleQuestions: true
shuffleAnswers: true
---

# Fill in the blank: "__ patches are better for modifying simple, standard fields such as names or replica counts"

1. [x] Json6902
    > Good. The Json6902 patch is better for these instances, due to its fine-grained control over the path of the target field, the action to perform on it, and the resulting value.
1. [ ] StrategicMergePatch

# Fill in the blank: "__ patches are better for modifying specific list entries"

1. [ ] Json6902
    > While you can definitely use the Json6902 patch for this, it's limited to using the specific index of the list entry, which removes idempotency from the operation.
1. [x] StrategicMergePatch
    > Good. Because of the limitations that the Json6902 "path" operator provides, you can't get logic inside of array indexing, you can only give the path a location in the array. This is problematic as it isn't necessarily idempotent, whereas the StrategicMergePatch can handle more complex logic inside of arrays.

# True or False: The Json6902 patch is more reliable than the StrategicMergePatch most of the time

1. [x] True
    > Good. The Json6902 patch uses a standardized patching mechanism called "JSON RFC 6902", which performs more predictably and consistently than the underlying Kubernetes patching mechanism. Tend to prefer the Json6902 patch when possible.
1. [ ] False
    > Not quite. The Json6902 patch uses a standardized patching mechanism called "JSON RFC 6902", which performs more predictably and consistently than the underlying Kubernetes patching mechanism. Tend to prefer the Json6902 patch when possible.

# What is the following Kustomize patch doing?

\`\`\`yaml
patches:
    - target:
        kind: Deployment
        name: ignored
      patch: |-
        - op: remove
          path: /spec/template/spec/containers/0/env/-
\`\`\`

1. [x] Removing the final entry of the \`env\` list in the first container of all deployments
    > Good. The trailing "-" in the path indicates that the last element of the list should be removed. And the "ignored" name is just a placeholder, so this patch will apply to all Deployments.
1. [ ] Removing the final entry of the \`env\` list in the first container of the deployment named "ignored"
    > Not quite. The "ignored" name is just a placeholder, so this patch will apply to all Deployments.
1. [ ] Removing the entire \`env\` list in the first container of all deployments
    > Not quite. The "-" in the path indicates that only the last element of the list should be removed, not the entire list.
1. [ ] Removing the entire \`env\` list in the first container of the deployment named "ignored"
    > Not quite. The trailing "-" in the path indicates that only the last element of the list should be removed. The "ignored" name is just a placeholder, so this patch will apply to all Deployments.
`;

export { rawQuizdown }