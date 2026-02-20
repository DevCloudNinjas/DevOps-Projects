const rawQuizdown = `
---
shuffleQuestions: true
shuffleAnswers: true
---

# Fill in the blank: "__ is used in ValidatingAdmissionPolicy to define the validation logic"

1. [x] CEL (Common Expression Language)
    > Correct. CEL is used in ValidatingAdmissionPolicy to write expressions for validation logic, offering a powerful and flexible way to define rules.
1. [ ] JSON
    > Not quite. While JSON is used in Kubernetes, CEL is the language used for writing validation expressions in ValidatingAdmissionPolicy.

# True or False: ValidatingAdmissionPolicies can use external webhooks for validation

1. [ ] True
    > Incorrect. ValidatingAdmissionPolicies are designed to perform validations in-process within the API server, without relying on external webhooks.
1. [x] False
    > Correct. ValidatingAdmissionPolicies perform validations in-process within the API server, providing better performance and reliability compared to external webhooks.

# What does the following CEL expression in a ValidatingAdmissionPolicy do?

\`\`\`cel
!('MY_KEY' in object.metadata.labels) || object.metadata.labels['MY_KEY'].matches('^[a-zA-Z]*$')
\`\`\`

1. [x] Validates that if a label 'MY_KEY' exists, its value contains only alphabetic characters
    > Correct. This expression checks if 'MY_KEY' is present in labels, and if so, ensures its value matches the regex for alphabetic characters only.
1. [ ] Requires that all labels contain only alphabetic characters
    > Not quite. This expression only checks the 'MY_KEY' label, not all labels.
1. [ ] Ensures that 'MY_KEY' label always exists with alphabetic characters
    > Incorrect. The expression allows for the absence of 'MY_KEY' label.
1. [ ] Removes any non-alphabetic characters from the 'MY_KEY' label
    > Not correct. This expression validates but does not modify the label value.

# What is the purpose of \`paramKind\` in a ValidatingAdmissionPolicy?

1. [x] To specify the kind of resource used in the policy expression
    > Correct. \`paramKind\` defines the type of resource that will be used to provide parameters to the policy, allowing for dynamic configuration.
1. [ ] To define the kinds of resources the policy will validate
    > Not quite. This is typically done in the \`matchConstraints\` section, not with \`paramKind\`.
1. [ ] To set default parameters for the policy
    > Incorrect. \`paramKind\` specifies the type of resource for parameters, it doesn't set default values.
1. [ ] To limit the namespaces where the policy applies
    > Not correct. Namespace limitations are typically set in the policy binding, not through \`paramKind\`.

# Suppose you CRD specified as \`paramKind\` and you did not specify a \`namespace\` in the \`paramRef\`. Which of the following statements are true? Select all that apply.

- [x] The API server will use the namespace of the object being evaluated for admission
    > Correct. When no namespace is specified in the paramRef for a namespaced CRD, the API server defaults to using the namespace of the object under evaluation.
- [x] This allows for a single binding to use different parameter resources in different namespaces
    > Correct. This behavior enables flexible, namespace-specific configurations using a single binding.
- [ ] The API server will use the default namespace
    > Not quite. The API server doesn't default to using the 'default' namespace in this scenario.
- [ ] The policy will fail to evaluate and return an error
    > Incorrect. The policy will still function, using the namespace of the object being evaluated.
- [x] The FailurePolicy of the ValidatingAdmissionPolicy is applied. 
    > Correct. If ParamRef does not specify a namespace  the API server will look for the ParamKind in the namespace of the object under evaluation. If ParamKind refers to a non-existent kind, this policy definition is mis-configured and the FailurePolicy is applied. See the [docs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#validatingadmissionpolicyspec-v1-admissionregistration-k8s-io)
- [ ] The policy will only apply to resources in the same namespace as the policy binding
    > Not correct. The policy can apply to resources in any namespace, using the respective namespace's parameter resource.

# What does the following \`matchConstraints\` configuration in a ValidatingAdmissionPolicy do?

\`\`\`yaml
matchConstraints:
  resourceRules:
  - apiGroups: ["apps"]
    apiVersions: ["v1"]
    operations: ["CREATE", "UPDATE"]
    resources: ["deployments", "statefulsets"]
\`\`\`

1. [x] Applies the policy to CREATE and UPDATE operations on deployments and statefulsets in the apps/v1 API group
    > Correct. This configuration specifically targets these resources and operations, limiting the scope of the policy's application.
1. [ ] Applies the policy to all operations on all resources in the apps/v1 API group
    > Not quite. The configuration specifies only certain operations and resources, not all.
1. [ ] Prevents CREATE and UPDATE operations on deployments and statefulsets
    > Incorrect. This configures when to apply the policy, not what the policy does.
1. [ ] Only allows CREATE and UPDATE operations on deployments and statefulsets
    > Not correct. This specifies when the policy applies, not what operations are allowed.

# How does CEL handle equality comparisons for arrays in ValidatingAdmissionPolicies?

1. [x] Arrays with list type 'set' or 'map' are compared ignoring element order
    > Correct. For these list types, CEL performs equality comparisons without considering the order of elements.
1. [ ] All arrays are always compared strictly, including element order
    > Not quite. CEL has special handling for certain list types in Kubernetes.
1. [ ] Arrays can never be directly compared for equality in CEL
    > Incorrect. CEL does allow array comparisons, with special rules for certain types.
1. [ ] Array equality is determined solely by length, not content
    > Not correct. The content of arrays is considered in equality comparisons, not just length.
`;

export { rawQuizdown }
