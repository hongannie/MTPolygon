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

[![Product Name Screen Shot][gauss-eq]](https://example.com)






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[gauss-eq]: images/screenshot.png
