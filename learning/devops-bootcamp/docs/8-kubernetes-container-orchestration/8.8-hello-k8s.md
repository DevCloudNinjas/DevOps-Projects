---
docs/8-kubernetes-container-orchestration/8.8-hello-k8s.md:
  category: Container Orchestration
  estReadingMinutes: 15
  exercises:
    -
      name: Kubernetes Custom Project
      description: Create a custom Kubernetes project, utilizing kubebuilder,Kubebuilder to create a kubernetes custom resource definition and controller which reconciles changes to the custom resource.
      estMinutes: 4800
      technologies:
      - Kubernetes
      - Custom Resources
      - Kubebuilder
---

# Hello K8s!

Now that you've had experience with the implementation and usage of a wider breadth of Kubernetes objects, it's time to take a deeper dive and put your knowledge to the test with a project of your own.

If you have been going through the bootcamp with others, now is the time to work on the project together.

<center>

## Requirements

This product can be anything you choose. However, there are some necessary components.

| Requirements                                                                                                                             |
|------------------------------------------------------------------------------------------------------------------------------------------|
| Utilize webhooks                                                                                                                         |
| Create a custom resource                                                                                                                 |
| Use [kubebuilder](https://github.com/kubernetes-sigs/kubebuilder) to create a controller which reconciles changes to the custom resource |

</center>

![ticket image](img8/ticket_light.svg ':size=100x100 :class=light-mode-icon :alt= ticket image; light mode')
![ticket image](img8/ticket_dark.svg ':size=100x100 :class=dark-mode-icon :alt= ticket image; dark mode')

# Deliverable

Once you have completed the application, you will be expected to not only demonstrate what you have done, but also what you learned while doing it. Do not simply talk about the end result, talk about the places you got stuck and how you got past those roadblocks. It can be very beneficial to include links to useful material that you used to learn about the subject matter. It is essential that you take time to prepare yourself before this presentation to ensure that you have a clear idea of what you want to say and what you want to demonstrate. As with any sort of public speaking, remaining relaxed and confident is very important, and remember to have fun with this. The audience is not judging you, they are just curious in what you've been working on.

# Tips

- Complete the Kubebuilder quickstart [kubebuilder](https://book.kubebuilder.io/quick-start).

- Briefly read through the [kubebuilder Book Tutorial sections 1.1-1.11](https://book.kubebuilder.io/cronjob-tutorial/cronjob-tutorial)

- Use the [kube builder deploy image plugin](https://book.kubebuilder.io/plugins/deploy-image-plugin-v1-alpha) to create a custom resource definition, custom resource, and controller.
