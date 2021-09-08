# Microtubule Polygon Fragmentation

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#introduction">Introduction</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#methods-and-data">Methods and Data</a>
      <ul>
        <li><a href="#gaussian-filter">Gaussian Filter</a></li>
        <li><a href="#image-enhancement">Image Enhancement</a></li>
        <li><a href="#image-cleanup">Image Clean-up</a></li>
        <li><a href="#obtaining-polygon-areas">Obtaining Polygon Areas</a></li>
      </ul>
    </li>
    <li><a href="#conclusions">Conclusions and Future Experiments</a></li>
  </ol>
</details>

<!-- INTRODUCTION -->
## Introduction

An individual skeletal muscle consists of multiple bundles of muscle fibers. Differentiation of skeletal muscle begins with myogenesis, the fusion of multiple myoblasts into a myotube where nuclei are positioned at the center of the myotube cell. As the myotube develops into a mature muscle fiber, nuclei migrate to the periphery of the cell such that they are maximally distanced from each other (Das, M., Wilson, K., Molnar, P. et al., 2007). 

However, individuals with muscular dystrophies are often characterized by aberrant positioning of nuclei, such as clustering or remaining near the center as in centronuclear myopathies. We use Drosophila melanogaster as our model system to study the nuclear positioning process in relation to muscle development. The structure and processes within skeletal muscle are highly conserved between humans and drosophila. Additionally, because each muscle cell in Drosophila is considered to be a muscle itself, this greatly reduces the complexity associated with bundled muscle fibers in human skeletal muscle (Auld et. al., 2018). 

It has been observed that mutations in the proteins ensconsin/MAP7 and dystrophin result in unusual positioning of nuclei. Dystrophin is a cytoplasmic protein that links the actin cytoskeleton to proteins along the muscle fiber membrane. Mutations in the dystrophin gene often result in well-known muscle diseases like Duchenne and Becker muscular dystrophy. Inability to produce functional dystrophin leads to “chronic muscle damage, inflammation and eventually replacement of muscle fibres by fat and fibrotic tissue and thus loss of muscle function” (Aartsma-Rus, Annemieke et al., 2016). Like dystrophin, ensconsin is a microtubule-associated protein and mutations in ensconsin can result in defective nuclear positioning. (Metzger, Thomas et al., 2012). 

Experiments have been performed to examine the phenotypes in ensconsin and dystrophin mutants. We have observed that the microtubule network around such nuclei appear different when compared with controls. In order to explore this, we decided to use advanced visualization analysis and computer vision techniques to examine and compare the microtubule network complexity surrounding individual nuclei in ensconsin and dystrophin mutants.

### Built With

Major frameworks used to build the code:

* [Python](https://www.python.org/)
* [numpy](https://numpy.org/)
* [OpenCV](https://opencv.org/)
* [skimage](https://scikit-image.org/)

<!-- METHODS AND DATA -->
## Methods and Data

### Gaussian Filter

A Gaussian smoothing operator was applied to blur images and remove background detail and noise. The 2D convolution operator uses the following equation:

O(i.j) =k=1ml=1nI(i+k-1,j+l-1)K(l,l)

k represents the kernel, a smaller matrix of values which slides over a larger matrix l (of the image itself). Each kernel position corresponds to a single output pixel, the value of which is calculated by multiplying together the kernel value and the underlying image pixel value for each of the cells in the kernel, and then adding all these numbers together.

Figure 1. Application of gaussian filter. From right to left: nuclei of ens_swo/+; ens_swo/+, Dys_EP3397/+; Dys_EP3397/+ mutants.

### Image Enhancement

An enhancement filter (indicated as the “tubeness algorithm” in the code) was implemented to selectively amplify the intensity profile and structure of the microtubules in the image. These filters are scalar functions :RR that analyze 2nd order intensity derivatives which are encoded in a Hessian matrix. 

If we let I(x) denote the intensity of a 2-dimensional image at coordinate x=[x1, x2]T, then the Hessian of I(x) at scale s is represented by a 2 by 2 matrix defined as:

Hi,j(x,s)=s2I(x)*∂2∂xi∂xjG(x,s)  for i,j = 1,2 

G(x,s) is the gaussian filter described above ( G(x,s)=122e-(x2+s2)/22) and the * symbol represents convolution. All four filters use this and then can be decomposed to VDVTto find the eigenvectors.

Four filters: Meijering, Frangi, Hessian, Sato were tested.  

Figure 2. Tubeness algorithms were applied after the initial gaussian filter for nuclei Dys_EP3397/+ mutants. From left to right: Meijering, Frangi, Hessian, Sato.

Meijering and Sato yield nearly identical outcomes, with similar identification profiles of microtubules. No results were observed after Frangi was implemented. The output for the Hessian algorithm does not match the original image observed in Fig. 1 (rightmost). Moving forwards, the Meijering filter was applied for all images.

The tubeness algorithm F(x) can be represented as:

F(x)=sup[eigH(x,s)]:sminssmax

v is the enhancement filter Meijering and smin and smax values are chosen to best represent the image. Calculation of all microtubules are based on how “elliptical” they are. Elliptical shape and properties are measured by the 1/2eigenvector ratio. As this fraction approaches infinity, the distribution becomes increasingly linear whereas if the fraction were to approach 0, then it would represent a circular distribution. In Fig. 2, the smin and smax value have been defined as smin = 3 and smax = 10. The smax and smin values are meant to mirror the 1 and 2values in the eigenvector ratio.

We can alter the smin and smax values to test which values best represent microtubule network profile from the original image. 

Figure 3. Differing values for smax and smin were set for the Meijering filter applied to the same nuclei of a Dys_EP3397/+ mutant. From left to right: smin = 3, smax = 10; smin = 5, smax = 10; smin = 3, smax = 7.

It appears that increasing the smin value promotes interconnectedness of microtubules and filters our smaller fragments while decreasing the smax value results in shorter fragments.

### Image Cleanup
The image was then binarized by calling the binarize function in ski-image. Fragments of 10 pixels and less were removed from the image using remove_small_objects from ski-image. Then microtubules were elongated by closing gaps of 5 pixels of less. Finally, the image was skeletonized via binary erosion.

Figure 4. Image clean up for nuclei of a Dys_EP3397/+ mutant. From left to right: (1) Meijering filter applied with smin = 3, smax = 10; (2) Image was binarized and small fragments were removed; (3) Gaps of 5 pixels or less were closed; (4) Skeletonize the image.

### Obtaining Polygon Areas
Polygon labeled and obtained using the regionprops function from ski-image.

Figure 5. Obtaining polygon areas from the MT network around the nuclei of a Dys_EP3397/+ mutant. From left to right: (1) Skeletonized image; (2) Polygons areas are obtained and shaded in; (3) Overlay of polygons and original image.

<!-- CONCLUSIONS -->
## Conclusions

Of all the four algorithms, Meijering and Sato look to be the most effective tubeness algorithm. Further experiments to follow with other values.

Observations show that ens_swo/+, Dys_EP3397/+ double mutants exhibit polarization of microtubules toward, but this has yet to be proven using the data gathered from the code. Currently, the code is built on the hypothesis that areas with high density of microtubules will have smaller polygon sizes. Because the microtubules are clustered so tightly together, the computer may treat multiple closely intersecting microtubules as a single entity. To supplement the polygon data, we could look into examining the intensity or density profiles. 

Previously when we analyzed the control data, we found that the control had smaller polygon sizes than expected and did not fit the prediction that we had. In Fig. 6, it looks like there aren’t as many microtubules in the raw images (topmost), when we run the control data with the code, we pick up a lot of the faint signal. 

Furthermore, we could look into 3D analysis to obtain a more accurate representation of the microtubule networks.
